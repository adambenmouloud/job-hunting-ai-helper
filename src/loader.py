import os
from typing import Dict


def get_resumes() -> Dict[str, str]:
    """Returns a mapping of resume names to their file paths."""
    resume_dir = "data/personal"
    if not os.path.exists(resume_dir):
        return {}

    resumes = {}
    for f in os.listdir(resume_dir):
        if f.endswith(".txt"):
            name = f.replace(".txt", "").replace("_", " ").replace("-", " ").title()
            resumes[name] = os.path.join(resume_dir, f)
    return resumes


def get_prompts() -> Dict[str, str]:
    """Returns a mapping of prompt names to their file paths."""
    prompt_dir = "data/prompts"
    if not os.path.exists(prompt_dir):
        return {}

    prompts = {}
    for f in os.listdir(prompt_dir):
        if f.endswith(".txt"):
            name = f.replace(".txt", "").replace("_", " ").replace("-", " ").title()
            prompts[name] = os.path.join(prompt_dir, f)
    return prompts


def load_resume(file_path: str) -> str:
    """Reads the content of a resume text file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Resume file not found at {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_prompt(prompt_name: str) -> str:
    """Reads a prompt template from the data/prompts directory."""
    path = os.path.join("data", "prompts", f"{prompt_name}.txt")
    if not os.path.exists(path):
        return ""

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_resumes() -> Dict[str, str]:
    """Loads all resumes into a dictionary mapping names to content."""
    resumes = get_resumes()
    return {name: load_resume(path) for name, path in resumes.items()}


def load_prompts() -> Dict[str, str]:
    """Loads all prompts into a dictionary mapping names to content."""
    prompts = get_prompts()
    return {name: load_resume(path) for name, path in prompts.items()}
