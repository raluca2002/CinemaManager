from Domain.film import Film


def test_film():
    film = Film("1009", "Pistruiatul", 1975, 24.99, True)
    assert film.id_entity == "1009"
    assert film.titlu == "Pistruiatul"
    assert film.an_aparitie == 1975
    assert film.pret_bilet == 24.99
    assert film.in_program is True

    film.id_entity = "1010"
    film.titlu = "B.D. in alerta"
    film.an_aparitie = 1978
    film.pret_bilet = 19.99
    film.in_program = False

    assert film.id_entity == "1010"
    assert film.titlu == "B.D. in alerta"
    assert film.an_aparitie == 1978
    assert film.pret_bilet == 19.99
    assert film.in_program is False
