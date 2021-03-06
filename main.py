import streamlit as st
import pymorphy2
import re
import textwrap

cases = dict(
    [
        ("gent", ("родительный", True)),
        ("datv", ("дательный", True)),
        ("accs", ("винительный", False)),
        ("ablt", ("творительный", False)),
        ("loct", ("предложный", False)),
    ]
)


def inflect(word, case):
    forms = morph.parse(word)
    # assume that initial string in nomn

    w = next((f for f in forms if "nomn" in f.tag), forms[0])
    try:
        return w.inflect({case}).word.capitalize()
    except:
        return word


morph = pymorphy2.MorphAnalyzer()

st.title("ФИО Склоняльщик")
st.sidebar.header("Какие падежи нужны")
st.markdown(
    textwrap.dedent(
        """\
    Склоняю фамилии-имена-отчества (и любые другие слова) из именительного падежа в какой надо.
    
    *Написано Ильёй Щуровым в 2020 году с использованием 
    [pymorphy2](https://pymorphy2.readthedocs.io/en/latest/) и 
    [streamlit](https://www.streamlit.io), исходники на 
    [github](http://github.com/ischurov/incline-fio).*
    """
    )
)

text = st.text_area(
    "Список склоняемых ФИО (именительный падеж)",
    textwrap.dedent(
        """\
                    Иванов Петр Петрович
                    Афанасьева Василиса Петровна
        """
    ),
)

use_cases = {
    case: st.sidebar.checkbox(label=case_name, value=default)
    for case, (case_name, default) in cases.items()
}

st.button("Склонять")
for case, use in use_cases.items():
    if use:
        st.text_area(
            cases[case][0],
            re.sub("[а-яА-Я]+", lambda m: inflect(m.group(0), case), text),
        )
