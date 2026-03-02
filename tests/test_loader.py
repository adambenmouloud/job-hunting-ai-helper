import pytest

from src.loader import get_resumes, load_prompt, load_resume


def test_get_resumes_missing_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert get_resumes() == {}


def test_get_resumes_returns_typ_only(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    personal = tmp_path / "data" / "personal"
    personal.mkdir(parents=True)
    (personal / "my_resume.typ").write_text("content")
    (personal / "notes.txt").write_text("ignore")
    result = get_resumes()
    assert len(result) == 1
    assert "My Resume" in result


def test_get_resumes_formats_name(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    personal = tmp_path / "data" / "personal"
    personal.mkdir(parents=True)
    (personal / "software_engineer-cv.typ").write_text("content")
    result = get_resumes()
    assert "Software Engineer Cv" in result


def test_load_resume_raises_if_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_resume(str(tmp_path / "nonexistent.typ"))


def test_load_resume_returns_content(tmp_path):
    f = tmp_path / "resume.typ"
    f.write_text("hello typst")
    assert load_resume(str(f)) == "hello typst"


def test_load_prompt_returns_empty_if_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert load_prompt("nonexistent") == ""


def test_load_prompt_returns_content(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    prompts = tmp_path / "data" / "prompts"
    prompts.mkdir(parents=True)
    (prompts / "my_prompt.txt").write_text("you are helpful")
    assert load_prompt("my_prompt") == "you are helpful"
