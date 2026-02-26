from pathlib import Path


def get_resumes() -> dict[str, str]:
    """Returns a mapping of resume names to their file paths."""
    resume_dir = Path("data/personal")
    if not resume_dir.exists():
        return {}

    resumes = {}
    for f in resume_dir.glob("*.typ"):
        name = f.stem.replace("_", " ").replace("-", " ").title()
        resumes[name] = str(f)
    return resumes


def load_resume(file_path: str) -> str:
    """Reads the content of a Typst resume file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Resume file not found at {file_path}")

    return path.read_text(encoding="utf-8")


def load_prompt(prompt_name: str) -> str:
    """Reads a prompt template from the data/prompts directory."""
    path = Path("data") / "prompts" / f"{prompt_name}.txt"
    if not path.exists():
        return ""

    return path.read_text(encoding="utf-8")
