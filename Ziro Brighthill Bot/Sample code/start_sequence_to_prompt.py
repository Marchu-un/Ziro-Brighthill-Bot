#Пример преобразования начальной последовательности вопросов в промпт.
#Требуется чтобы данные из начальной последовательности вопросов имели такие типы, как приведено тут
charcters = {123445: "Эльф Леголас", 54321: "Гном Пиборас"}

game_world = "Мрачное средневековье"

wishes = "Харизматичный гейммастер"

characters_to_str = " и ".join(charcters.values())

Brighthill_initial_prompt = f"Я - гейммастер для игры по мотивам dungeons & dragons. Моё имя Зиро Брайтхил.Я провожу игру для игроков {characters_to_str}. Мир игры: {game_world}. Пожелания игроков: {wishes}."

print (Brighthill_initial_prompt)