#include "treenode.h"
#include <string>
using namespace std;

TreeNode* TreeNode::insert(pair<string, string> wordPair) {
    if (wordPair < this->words_) {
        if (left_) {
            left_ = left_->insert(wordPair);
        }
        else {
            left_ = new TreeNode(wordPair);
        }
    }
    else {
        if (right_) {
            right_ = right_->insert(wordPair);
        }
        else {
            right_ = new TreeNode(wordPair);
        }
    }
    return this;
}

TreeNode* TreeNode::remove(pair<string, string> words) {
    if (words.first < words_.first) {
        if (left_) left_ = left_->remove(words);
        return this;
    }
    if (words.first > words_.first) {
        if (right_) right_ = right_->remove(words);
        return this;
    }

    if (!left_ && !right_) {
        delete this;
        return nullptr;
    }

    if (!left_) return right_;
    if (!right_) return left_;

    TreeNode* succ = right_;
    while (succ->left_) succ = succ->left_;

    words_ = succ->words_; // копируем данные successor
    right_ = right_->remove(succ->words_); // безопасно удаляем successor рекурсивно
    return this;
}

int TreeNode::nodeCount() {
    int leftCount = left_ ? left_->nodeCount() : 0;
    int rightCount = right_ ? right_->nodeCount() : 0;
    return 1 + leftCount + rightCount;
}

TreeNode* TreeNode::getLeft()  const {
    return left_;
}
TreeNode* TreeNode::getRight()  const {
    return right_;
}
pair<string, string> TreeNode::getPair()  const {
    return words_;
}
void TreeNode::setLeft(TreeNode* left) {
    left_ = left;
}
void TreeNode::setRight(TreeNode* right) {
    right_ = right;
}
void TreeNode::setPair(pair<string, string> words) {
    words_ = words;
}

TreeNode* TreeNode::find(string en) {
    if (words_.first == en) return this;
    if (en < words_.first) {
        return left_ ? left_->find(en) : nullptr;
    }
    else {
        return right_ ? right_->find(en) : nullptr;
    }
}

string& TreeNode::getRuAdress() {
    return words_.second;
}

//TreeNode::TreeNode() {
//    left_ = right_ = nullptr;
//    words_ = { "", "" };
//}

TreeNode::TreeNode(pair<string, string> words) {
    left_ = right_ = nullptr;
    words_ = words;
}

//TreeNode::~TreeNode() {
//    // безопасное рекурсивное удаление
//    if (left_) {
//        delete left_;
//        //left_ = nullptr;
//    }
//    if (right_) {
//        delete right_;
//        //right_ = nullptr;
//    }
//}

bool TreeNode::operator==(const TreeNode& other) const {
    return words_ == other.words_;
}

bool TreeNode::operator!=(const TreeNode& other) const {
    return !(*this == other);
}

// Конструктор копирования (глубокое копирование)
//TreeNode::TreeNode(const TreeNode& other) {
//    words_ = other.words_;
//    left_ = right_ = nullptr;
//    if (other.left_) left_ = new TreeNode(*other.left_);
//    if (other.right_) right_ = new TreeNode(*other.right_);
//}
//
//// Оператор присваивания (глубокое копирование)
//TreeNode& TreeNode::operator=(const TreeNode& other) {
//    if (this == &other) return *this;
//
//    // удалить текущие поддеревья
//    delete left_;
//    delete right_;
//    left_ = right_ = nullptr;
//
//    words_ = other.words_;
//    if (other.left_) left_ = new TreeNode(*other.left_);
//    if (other.right_) right_ = new TreeNode(*other.right_);
//    return *this;
//}
