#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path
import pathlib


def get_poezd(poezd, name, no, time):
    """
    Добавить данные о поезде
    """
    poezd.append({"name": name, "no": no, "time": time})
    return poezd


def list(poezd):
    """
    Отобразить список поездов
    """
    # проверить, что список поездов не пуст
    if poezd:
        line = "+-{}-+-{}-+-{}-+".format(
            "-" * 10,
            "-" * 20,
            "-" * 8,
        )
        print(line)
        print("| {:^10} | {:^20} | {:^8} |".format(" No ", "Название", "Время"))
        print(line)

        for idx, po in enumerate(poezd, 1):
            print(
                "| {:>10} | {:<20} | {"
                "} |".format(po.get("no", ""), po.get("name", ""), po.get("time", ""))
            )
        print(line)

    else:
        print("Список поездов пуст.")


def select_poezd(poezd, nom):
    """
    Выбор поездов по номеру
    """
    rezult = []
    for idx, po in enumerate(poezd, 1):
        if po["no"] == str(nom):
            rezult.append(po)

    return rezult


def save_poezd(file_name, poezd):
    """
    Сохранить список поездов в json-файл
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат json.
        json.dump(poezd, fout, ensure_ascii=False, indent=4)
    directory = pathlib.Path.cwd().joinpath(file_name)
    directory.replace(pathlib.Path.home().joinpath(file_name))


def load_poezd(file_name):
    """
    Считать список поездов из json-файла
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    # Создаем основной парсер командной строки
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument("filename", action="store", help="Имя файла данных")

    parser = argparse.ArgumentParser("poezd")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser("add", parents=[file_parser], help="Добавить поезд")
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="Название пункта назначения?",
    )
    add.add_argument("--no", action="store", type=int, help="Номер поезда?")
    add.add_argument(
        "-t", "--time", action="store", required=True, help="Время отправления?"
    )

    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Панель отображения поездов"
    )

    #Создать субпарсер для выбора поездов.
    select = subparsers.add_parser(
        "select", parents=[file_parser], help="Выбор поезда по номеру"
    )
    select.add_argument(
        "-o",
        "--nom",
        action="store",
        type=int,
        required=True,
        help="Введите номер поезда",
    )

    args = parser.parse_args(command_line)

    # Загрущить список поездов из файла, если он существует
    is_dirty = False
    if os.path.exists(args.filename):
        poezd = load_poezd(args.filename)
    else:
        poezd = []

    if args.command == "add":
        poezd = get_poezd(poezd, args.name, args.no, args.time)
        is_dirty = True

    # Отобразить список поездов
    elif args.command == "display":
        list(poezd)

    elif args.command == "select":
        selected = select_poezd(poezd, args.nom)
        list(selected)

    if is_dirty:
        save_poezd(args.filename, poezd)


if __name__ == "__main__":
    main()
    