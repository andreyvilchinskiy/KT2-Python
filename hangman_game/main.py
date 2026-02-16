import hangman_module


def main() -> None:
    hangman_module.initialize_game()
    game_info = hangman_module.get_game_info()
    hangman_module.display_output(game_info)

    while True:
        if game_info['is_won'] or game_info['is_lost']:
            user_choice = hangman_module.get_user_input(
                "\nХотите сыграть еще? (да/нет): "
            )

            if user_choice.lower() == 'да':
                game_info = hangman_module.restart_game()
                hangman_module.display_output(game_info)
            else:
                hangman_module.display_goodbye()
                break
        else:
            user_input = hangman_module.get_user_input("\nВведите букву: ")
            game_info = hangman_module.make_move(user_input)
            hangman_module.display_output(game_info)


if __name__ == "__main__":
    main()