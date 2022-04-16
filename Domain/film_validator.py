from Domain.film import Film


class FilmValidationError(Exception):
    pass


class FilmValidator:
    @staticmethod
    def validate(film: Film):
        errors = []
        if len(film.id_entity) == 0:
            errors.append("ID-ul nu poate fi vid!")
        if film.pret_bilet < 0:
            errors.append("Pretul biletului trebuie sa fie un numar pozitiv!")
        if film.an_aparitie < 0:
            errors.append("Anul de aparatie nu poate sa fie un numar negativ!")
        if len(errors) != 0:
            raise FilmValidationError(errors)
