#include <iostream>
#include <string>
#include <fstream>
#include <locale.h>
#define NOMINMAX
#include <windows.h>
#include "treenode.h"
#include "dict.h"
#include "menu.h"
//#pragma execution_character_set("utf-8")
using namespace std;

int main()
{
    setlocale(LC_ALL, "ru");
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);

    Dict dict;
    Menu menu;
    int choice;

    while (true) {
        menu.displayMenu();
        choice = menu.getNumericInput();

        switch (choice) {
        case 1: { // Добавить слово
            string en = menu.getStringInput(WORD_PROMT);
            string ru = menu.getStringInput(TRANSLATION_PROMT);
            dict += make_pair(en, ru);
            cout << "Слово добавлено!" << endl;
            break;
        }

        case 2: { // Удалить слово
            string en = menu.getStringInput(WORD_PROMT);
            dict -= make_pair(en, "<отсутствует>");
            cout << "Слово удалено." << endl;
            break;
        }

        case 3: { // Найти перевод
            string en = menu.getStringInput(WORD_PROMT);
            cout << dict[en] << endl;
            break;
        }

        case 4: { // Заменить перевод
            string en = menu.getStringInput(WORD_PROMT);
            string ru = menu.getStringInput(TRANSLATION_PROMT);
            dict[en] = ru;
            cout << "Перевод \"" << ru << "\" добавлен в словарь." << endl;
            break;
        }

        case 5: { // Количество слов
            if(dict.empty()) cout << "Словарь пуст." << endl;
            else cout << "Количество слов: " << dict.getRoot()->nodeCount() << endl;
            break;
        }

        case 6: { // Загрузка из файла
            string fname = menu.getStringInput(FILENAME_PROMT);
            ifstream file(fname);
            if (file) {
                file >> dict;
                cout << "Словарь загружен." << endl;
            }
            else cout << "Ошибка загрузки." << endl;
            break;
        }

        case 7: { // Выход
            cout << "Выход из программы..." << endl;
            return 0;
        }

        default:
            cout << "Некорректный ввод. Повторите попытку." << endl;
            break;
        }
        cout << "\n";
    }
}

void Menu::displayMenu() {
    std::cout << "\n=== АНГЛО-РУССКИЙ СЛОВАРЬ ===\n";
    std::cout << "1. Добавить слово и перевод\n";
    std::cout << "2. Удалить слово\n";
    std::cout << "3. Найти перевод\n";
    std::cout << "4. Заменить перевод\n";
    std::cout << "5. Показать количество слов\n";
    std::cout << "6. Загрузить словарь из файла\n";
    std::cout << "7. Выход\n";
}

int Menu::getNumericInput() {
    int a;
    while (true) {
        cout << "Введите число: ";
        try {
            if (!(cin >> a) || a > 7 || a < 1) {
                throw invalid_argument("Ошибка ввода");
            }
            return a;
        }
        catch (const invalid_argument& e) {
            cout << e.what() << endl;
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }
    }
}

string Menu::getStringInput(const string promt) {
    string input;
    while (true) {
        try {
            cout << promt;
            if (!(cin >> input) || input.empty()) {
                throw invalid_argument("Ошибка ввода");
            }

            return input;
        }
        catch (const invalid_argument& e) {
            cout << e.what() << endl;
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }
    }
}

pair<string, string> split(string str, char separator) {
    int pos = str.find(separator);
    return make_pair<string, string>(str.substr(0, pos), str.substr(pos + 1));
}

