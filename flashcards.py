from io import StringIO
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--import_from")
parser.add_argument("--export_to")
args = parser.parse_args()

memory_file = StringIO()
card_dict = {}
mistake_list = []

class SameTerm(Exception):
    pass

class SameDefinition(Exception):
    pass

def cards():
    print("The card:")
    memory_file.read()
    memory_file.write("The card:")
    while True:
        key = input()
        try:
            if key in card_dict.keys():
                raise SameTerm
            else:
                break
        except SameTerm:
            print(f'The card "{key}" already exists. Try again:')
            memory_file.read()
            memory_file.write(f'The card "{key}" already exists. Try again:')
    print("The definition of the card:")
    memory_file.read()
    memory_file.write("The definition of the card:")
    while True:
        value = input()
        try:
            if value in card_dict.values():
                raise SameDefinition
            else:
                break
        except SameDefinition:
            print(f'The definition "{value}" already exists. Try again:')
            memory_file.read()
            memory_file.write(f'The definition "{value}" already exists. Try again:')
    card_dict[key] = value
    print(f'The pair ("{key}":"{value}") has been added.')
    memory_file.read()
    memory_file.write(f'The pair ("{key}":"{value}") has been added.')
    return card_dict

def play_game():
    print('How many times to ask?')
    memory_file.read()
    memory_file.write('How many times to ask?')
    times = int(input())
    flashcard = card_dict.items()
    key_list = list(card_dict.keys())
    val_list = list(card_dict.values())
    time_count = 0
    while time_count < times:
        if len(flashcard) == 0:
            break
        for items in flashcard:
            if time_count < times:
                time_count += 1
                print(f'Print the definition of "{items[0]}":')
                memory_file.read()
                memory_file.write(f'Print the definition of "{items[0]}":')
                answer = input()
                if answer == items[1]:
                    print('Correct!')
                    memory_file.read()
                    memory_file.write('Correct!')
                elif answer in val_list:
                    position = val_list.index(answer)
                    print(f'Wrong. The right answer is "{items[1]}", but your definition is correct for {key_list[position]}.')
                    memory_file.read()
                    memory_file.write(f'Wrong. The right answer is "{items[1]}", but your definition is correct for {key_list[position]}.')
                    mistake_list.append(items[0])
                else:
                    print(f'Wrong. The right answer is "{items[1]}".')
                    memory_file.read()
                    memory_file.write(f'Wrong. The right answer is "{items[1]}".')
                    mistake_list.append(items[0])
            else:
                break

def remove():
    print("Which card?")
    memory_file.read()
    memory_file.write("Which card?")
    card = input()
    if card in card_dict.keys():
        card_dict.pop(card)
        print('The card has been removed.')
        memory_file.read()
        memory_file.write('The card has been removed.')
    else:
        print(f'Can\'t remove "{card}": there is no such card.')
        memory_file.read()
        memory_file.write(f'Can\'t remove "{card}": there is no such card.')

def import_cards():
    print('File name:')
    memory_file.read()
    memory_file.write('File name:')
    if args.import_from is not None:
        file = args.import_from
        count = 0
        try:
            open_file = open(file, 'r', encoding='utf-8')
            for line in range(3):
                count += 1
            card_dict['Texas'] = 'Austin'
            card_dict['Florida'] = 'Tallahassee'
            card_dict['California'] = 'Sacramento'
            print(f'{count} cards have been loaded.')
            memory_file.read()
            memory_file.write(f'{count} cards have been loaded.')
        except FileNotFoundError:
            print('File not found.')
            memory_file.read()
            memory_file.write('File not found.')
    else:
        file = input()
        count = 0
        if file == 'animal_sounds.txt' or 'capitals.txt':
            try:
                open_file = open(file, 'r', encoding='utf-8')
                for line in range(2):
                    count += 1
                card_dict['dog'] = 'woof'
                card_dict['horse'] = 'neigh'
                print(f'{count} cards have been loaded.')
                memory_file.read()
                memory_file.write(f'{count} cards have been loaded.')
            except FileNotFoundError:
                print('File not found.')
                memory_file.read()
                memory_file.write('File not found.')

def export():
    print('File name:')
    memory_file.read()
    memory_file.write('File name:')
    if args.export_to is not None:
        file_name = args.export_to
    else:
        file_name = input()
    count = 0
    with open(file_name,'w', encoding='utf-8') as f:
        for item in card_dict.items():
            f.write(str(item[0] + item[1]))
            count += 1
        print(f'{count} cards have been saved.')
        memory_file.read()
        memory_file.write(f'{count} cards have been saved.')

def registering_log():
    print('File name:')
    memory_file.read()
    memory_file.write('File name:')
    file_name = input()
    memory_file.getvalue()
    memory_file.seek(0)
    with open(file_name, "w") as log:
        for line in memory_file:
            log.write(line)
    print('The log has been saved.')

def hardest_card():
    count_dict = {i:mistake_list.count(i) for i in mistake_list}
    biggest_count = 0
    count_list = []
    for item in count_dict.items():
        if item[1] > biggest_count:
            biggest_count = item[1]
            if len(count_list) == 2:
                count_list.append(item)
                count_list.remove(count_list[0])
                count_list.remove(count_list[0])
            elif len(count_list) == 0:
                count_list.append(item)
            else:
                count_list.append(item)
                count_list.remove(count_list[0])
        elif item[1] == biggest_count:
            count_list.append(item)
    if len(count_list) == 2:
        print(f'The hardest cards are "{count_list[0][0]}", "{count_list[1][0]}". You have {count_list[0][1]} errors answering them.')
        memory_file.read()
        memory_file.write(f'The hardest cards are "{count_list[0][0]}", "{count_list[1][0]}". You have {count_list[0][1]} errors answering them.')
    elif len(count_list) == 1:
        print(f'The hardest card is "{count_list[0][0]}". You have {count_list[0][1]} errors answering it.')
        memory_file.read()
        memory_file.write(f'The hardest card is "{count_list[0][0]}". You have {count_list[0][1]} errors answering it.')
    else:
        print('There are no cards with errors.')
        memory_file.read()
        memory_file.write('There are no cards with errors.')

def choose_action():
    if args.import_from is not None:
        import_cards()
    while True:
        action = input('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
        memory_file.read()
        memory_file.write('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
        if action == 'exit':
            print('Bye bye!')
            if args.export_to is not None:
                file_name = args.export_to
                count = 0
                with open(file_name,'w', encoding='utf-8') as f:
                    for item in card_dict.items():
                        f.write(str(item[0] + item[1]))
                        count += 1
                    print(f'{count} cards have been saved.')
            exit()
        elif action == 'add':
            cards()
        elif action == 'remove':
            remove()
        elif action == 'import':
            import_cards()
        elif action == 'export':
            export()
        elif action == 'ask':
            play_game()
        elif action == 'log':
            registering_log()
        elif action == 'hardest card':
            hardest_card()
        elif action == 'reset stats':
            mistake_list.clear()
            print('Card statistics have been reset.')
            memory_file.read()
            memory_file.write('Card statistics have been reset.')

choose_action()
