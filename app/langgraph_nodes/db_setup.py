# app/langgraph_nodes/db_setup.py

import os
import subprocess
from pathlib import Path
import re
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from app.utils.colors import GREEN, CYAN, YELLOW, RED, RESET, BOLD

def generate_db_models(srs_analysis: str, model=None) -> str:
    if not model:
        model = ChatOpenAI(
            model="llama3-70b-8192",
            temperature=0.2,
            openai_api_key=os.getenv("GROQ_API_KEY"),
            openai_api_base="https://api.groq.com/openai/v1",
        )

    prompt = f"""
Based on the following extracted backend requirements from an SRS, generate clean SQLAlchemy models (use Base = declarative_base()).
Use Python 3.12 syntax and type hints.

Return only valid Python code. Do not include markdown, triple backticks, or explanatory comments.

Requirements:
{srs_analysis}
    """

    response = model([
        SystemMessage(content="You are a backend engineer writing database models."),
        HumanMessage(content=prompt)
    ])

    return patch_enum_names(response.content)

def patch_enum_names(code: str) -> str:
    lines = code.splitlines()
    patched_lines = []
    enum_buffer = []
    inside_enum = False

    for line in lines:
        if 'Enum(' in line:
            inside_enum = True
            enum_buffer = [line]
            continue

        if inside_enum:
            enum_buffer.append(line)
            if ')' in line:
                enum_block = '\n'.join(enum_buffer)
                if 'name=' not in enum_block:
                    values = re.findall(r"'(\w+)'", enum_block)
                    enum_name = "enum_" + ("_".join(values)[:30] or "field")
                    new_enum = enum_block.rstrip(')').rstrip() + f", name='{enum_name}')"
                    patched_lines.append(new_enum)
                else:
                    patched_lines.extend(enum_buffer)
                inside_enum = False
                enum_buffer = []
            continue

        patched_lines.append(line)

    return '\n'.join(patched_lines)

def run_subprocess(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"{RED}❌ Error running command:{RESET} {cmd}")
        print(result.stderr.decode())
    else:
        print(f"{GREEN}✔️ Ran:{RESET} {CYAN}{cmd}{RESET}")
    return result

def db_setup_node(state: dict):
    print(f"\n{YELLOW}🔗 Setting up PostgreSQL DB and models for project: {CYAN}{state['project_name']}{RESET}")

    project_name = state["project_name"]
    project_path = Path(state["project_path"])
    models_dir = project_path / "app" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    db_name = f"db_{project_name}"
    db_user = f"user_{project_name}"
    db_pass = f"pass_{project_name}"
    db_container = f"pg_{project_name}"
    db_url_async = f"postgresql+asyncpg://{db_user}:{db_pass}@localhost:5432/{db_name}"
    db_url_sync = f"postgresql://{db_user}:{db_pass}@localhost:5432/{db_name}"

    check_container_cmd = f"podman ps -a --format '{{{{.Names}}}}' | grep -w {db_container}"
    result = subprocess.run(check_container_cmd, shell=True, stdout=subprocess.PIPE)

    if result.returncode != 0:
        print(f"{YELLOW}📦 Creating new Podman container: {CYAN}{db_container}{RESET}")
        podman_cmd = f"podman run --name {db_container} -e POSTGRES_USER={db_user} -e POSTGRES_PASSWORD={db_pass} -e POSTGRES_DB={db_name} -p 5432:5432 -d docker.io/library/postgres"
        run_subprocess(podman_cmd)
    else:
        print(f"{GREEN}✔️ Using existing Podman container: {CYAN}{db_container}{RESET}")
        run_subprocess(f"podman start {db_container}")

    models_code = generate_db_models(state["srs_analysis"])
    model_file_path = models_dir / "models.py"
    with open(model_file_path, "w") as f:
        f.write(models_code)
    print(f"{GREEN}  ✓ models.py written at: {CYAN}{model_file_path}{RESET}")

    db_path = project_path / "app" / "database.py"
    db_code = f"""from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
"""
    with open(db_path, "w") as f:
        f.write(db_code)
    print(f"{GREEN}  ✓ database.py written at: {CYAN}{db_path}{RESET}")

    env_path = project_path / ".env"
    with open(env_path, "w") as f:
        f.write(f"DATABASE_URL={db_url_async}\n")
    print(f"{GREEN}  ✓ Injected DATABASE_URL into: {CYAN}{env_path}{RESET}")

    alembic_dir = project_path / "alembic"
    env_py = alembic_dir / "env.py"

    if not env_py.exists():
        run_subprocess("alembic init alembic", cwd=project_path)
    else:
        print(f"{GREEN}✔️ Alembic already initialized: {CYAN}{alembic_dir}{RESET}")

    alembic_ini = project_path / "alembic.ini"
    if alembic_ini.exists():
        content = alembic_ini.read_text()
        patched = []
        for line in content.splitlines():
            if line.strip().startswith("sqlalchemy.url"):
                patched.append(f"sqlalchemy.url = {db_url_sync}")
            else:
                patched.append(line)
        alembic_ini.write_text("\n".join(patched))

    if env_py.exists():
        content = env_py.read_text()
        lines = content.splitlines()
        new_lines = []
        skip = False
        inserted_imports = False
        inserted_metadata = False

        for i, line in enumerate(lines):
            if line.strip() == "target_metadata = None":
                continue

            if line.strip().startswith("from alembic import context") and not inserted_imports:
                new_lines.append(line)
                new_lines.append("from sqlalchemy import create_engine")
                new_lines.append("from app.models.models import Base")
                inserted_imports = True
                continue

            if inserted_imports and not inserted_metadata and line.strip() == "":
                new_lines.append("target_metadata = Base.metadata")
                inserted_metadata = True

            if line.strip().startswith("def run_migrations_online"):
                new_lines.append("def run_migrations_online() -> None:")
                new_lines.append("    \"\"\"Run migrations in 'online' mode.\"\"\"")
                new_lines.append("    connectable = create_engine(config.get_main_option(\"sqlalchemy.url\"))")
                new_lines.append("    with connectable.connect() as connection:")
                new_lines.append("        context.configure(connection=connection, target_metadata=target_metadata)")
                new_lines.append("        with context.begin_transaction():")
                new_lines.append("            context.run_migrations()")
                skip = True
                continue

            if skip:
                if line.strip().startswith("if context.is_offline_mode()"):
                    skip = False
                    new_lines.append(line)
                continue

            new_lines.append(line)

        env_py.write_text("\n".join(new_lines))

    run_subprocess("alembic revision --autogenerate -m 'Initial schema'", cwd=project_path)
    run_subprocess("alembic upgrade head", cwd=project_path)

    print(f"\n{YELLOW}✅ Database setup complete. Models & migrations ready.{RESET}\n")

    return {
        **state,
        "db_models_path": str(model_file_path),
        "db_url": db_url_async,
        "db_setup_success": True
    }
