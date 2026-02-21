from pathlib import Path
from typing import Dict


def get_resumes() -> Dict[str, str]:
    """Returns a mapping of resume names to their file paths."""
    resume_dir = Path("data/personal")
    if not resume_dir.exists():
        return {}

    resumes = {}
    for f in resume_dir.glob("*.txt"):
        name = f.stem.replace("_", " ").replace("-", " ").title()
        resumes[name] = str(f)
    return resumes


def get_prompts() -> Dict[str, str]:
    """Returns a mapping of prompt names to their file paths."""
    prompt_dir = Path("data/prompts")
    if not prompt_dir.exists():
        return {}

    prompts = {}
    for f in prompt_dir.glob("*.txt"):
        name = f.stem.replace("_", " ").replace("-", " ").title()
        prompts[name] = str(f)
    return prompts


def load_resume(file_path: str) -> str:
    """Reads the content of a resume text file."""
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


def load_resumes() -> Dict[str, str]:
    """Loads all resumes into a dictionary mapping names to content."""
    resumes = get_resumes()
    return {name: load_resume(path) for name, path in resumes.items()}


def load_prompts() -> Dict[str, str]:
    """Loads all prompts into a dictionary mapping names to content."""
    prompts = get_prompts()
    return {name: load_resume(path) for name, path in prompts.items()}
