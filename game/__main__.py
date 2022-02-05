from game import Game


def main() -> None:
    g = Game()
    g.show_start_screen()
    g.new()
    g.run()
    g.show_go_screen()


if __name__ == "__main__":
    main()
