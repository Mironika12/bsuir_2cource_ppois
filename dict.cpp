#include "treenode.h" //???
#include "dict.h"
#include "menu.h"
#include <iostream>
#include <string>
#include <fstream>
using namespace std;

Dict& Dict::operator +=(const pair<string, string>& wordPair) {
    if (!root) root = new TreeNode(wordPair);
    else root->insert(wordPair);
    return *this;
}

Dict& Dict::operator -=(const pair<string, string>& words) {
    if (!this->empty()) {
        root = root->remove(words); // присваиваем возможно новый корень
    }
    return *this;
}

bool Dict::empty() {
    if (!this->root) return true;
    else return false;
}

TreeNode* Dict::getRoot() {
    return root;
}

string Dict::operator[](const string& en) const {
    if (!root) return "<отсутствует>";
    TreeNode* found = root->find(en);
    if (!found) return "<отсутствует>";
    return found->getPair().second;
}

string& Dict::operator[](const string& en) {
    TreeNode* node = root ? root->find(en) : nullptr;
    if (!node) {
        *this += {en, "<отсутствует>"};
        node = root->find(en);
    }
    return node->getRuAdress();
}

Dict::Dict() {
    root = nullptr;
}

Dict::Dict(pair<string, string> words) {
    root = new TreeNode(words);
}

Dict::~Dict() {
    delete root;
}

// Оператор вывода для записи словаря в файл
ostream& operator<<(std::ostream& os, const Dict& dict) {
    if (dict.root) {
        dict.outputDict(os, dict.root);
    }
    return os;
}

istream& operator>>(std::istream& is, Dict& dict) {
    if (dict.root) {
        delete dict.root;
        dict.root = nullptr;
    }

    dict.root = dict.inputDict(is);
    return is;
}

void Dict::outputDict(ostream& os, TreeNode* node) const {
    if (!node) {
        os << "NULL" << std::endl;
        return;
    }

    pair<string, string> pair = node->getPair();
    os << pair.first << "," << pair.second << std::endl;

    outputDict(os, node->getLeft());
    outputDict(os, node->getRight());
}

TreeNode* Dict::inputDict(istream& is) {
    string line;
    if (!getline(is, line) || line == "NULL") {
        return NULL;
    }

    int sepPos = line.find(SEPARATOR);
    string en = line.substr(0, sepPos);
    string ru = line.substr(sepPos + 1);
    TreeNode* node = new TreeNode(make_pair(en, ru));

    TreeNode* left = inputDict(is);
    if (left) {
        node->setLeft(left);
    }

    TreeNode* right = inputDict(is);
    if (right) {
        node->setRight(right);
    }

    return node;
}

static TreeNode* copyTree(const TreeNode* node) {
    if (!node) return nullptr;
    TreeNode* newNode = new TreeNode(node->getPair());
    newNode->setLeft(copyTree(node->getLeft()));
    newNode->setRight(copyTree(node->getRight()));
    return newNode;
}

Dict::Dict(const Dict& other) {
    if (other.root)
        root = copyTree(other.root);
    else
        root = nullptr;
}

Dict& Dict::operator=(const Dict& other) {
    if (this == &other)
        return *this;

    // Очистим текущее дерево
    delete root;

    // Глубокое копирование
    if (other.root)
        root = copyTree(other.root);
    else
        root = nullptr;

    return *this;
}
