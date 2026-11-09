"""Переименование Лира → Мира: на слух откликается на «Мира» и на прежнее «Лира», но «мира» как слово («для мира»,
«в мире») помощницу не будит — это родительный падеж слова «мир». Чистая проверка find_name / name_inside
(core/engine_base.py): HOMONYM_NAMES — имена, совпадающие с обычными словами."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
from engine_base import find_name, name_inside  # noqa: E402

fails = []


def ok(c, m):
    print(("✅ " if c else "❌ ") + m)
    if not c:
        fails.append(m)


AL = {"lira": ["мира", "лира"], "patrik": ["патрик"], "eva": ["эва"]}
ok(find_name("Мира, включи музыку", AL)[0] == "lira", "«Мира, включи музыку» — зовут")
ok(find_name("мира сколько время", AL, strict=True)[0] == "lira", "строгий режим: «мира сколько время»")
ok(find_name("эй мира какая погода", AL)[0] == "lira", "«эй мира…» — зовут")
ok(find_name("слушай мира, расскажи", AL)[0] == "lira", "«слушай, мира…» — зовут")
ok(find_name("Лира, включи музыку", AL)[0] == "lira", "прежнее имя «Лира, включи музыку» — зовут")
ok(find_name("лиру включи", AL)[0] == "lira", "«лиру включи» — падеж прежнего имени")
ok(find_name("Платформа открылась для мира, и теперь", AL)[0] is None, "«…для мира…» не будит")
ok(find_name("мы живём в мире где", AL)[0] is None, "«в мире» не будит")
ok(find_name("это лучшее для мира", AL)[0] is None, "«лучшее для мира» не будит")
ok(name_inside("Я так и начал. Мира, расскажи про погоду", AL) == "lira", "имя в начале второго предложения — зовут")
ok(name_inside("все мечтают о мире во всём мире, мира всем", AL) is None, "«о мире… мира всем» посреди речи — не обращение")
ok(name_inside("спроси у лиры, что там", AL) == "lira", "прежнее имя посреди речи («спроси у лиры») работает")
ok(find_name("Патрик, привет", AL)[0] == "patrik" and find_name("Эва, привет", AL)[0] == "eva", "остальные имена не пострадали")
print("\nИТОГ:", "всё прошло" if not fails else f"провалов {len(fails)}")
sys.exit(1 if fails else 0)
