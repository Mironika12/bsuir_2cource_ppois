#include "treenode.h"
#include <string>
using namespace std;

TreeNode* TreeNode::insert(pair<string, string> words) {
    if (words.first < words_.first) {
        if (left_) left_ = left_->insert(words);
        else left_ = new TreeNode(words);
    }
    else {
        if (right_) right_ = right_->insert(words);
        else right_ = new TreeNode(words);
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

    if (!left_) {
        TreeNode* r = right_;
        right_ = nullptr;
        delete this;
        return r;
    }

    if (!right_) {
        TreeNode* l = left_;
        left_ = nullptr;
        delete this;
        return l;
    }

    TreeNode* minInTree = right_;
    while (minInTree->left_) minInTree = minInTree->left_;

    words_ = minInTree->words_;
    right_ = right_->remove(minInTree->words_);
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
const pair<string, string>& TreeNode::getWords()  const {
    return words_;
}
pair<string, string>& TreeNode::getWords() {
    return words_;
}
void TreeNode::setLeft(TreeNode* left) {
    left_ = left;
}
void TreeNode::setRight(TreeNode* right) {
    right_ = right;
}
void TreeNode::setWords(pair<string, string> words) {
    words_ = words;
}

TreeNode* TreeNode::find(string en) {
    if (words_.first == en) return this;
    if (en < words_.first) return left_ ? left_->find(en) : nullptr;
    else return right_ ? right_->find(en) : nullptr;
}

TreeNode::TreeNode(pair<string, string> words) {
    left_ = right_ = nullptr;
    words_ = words;
}

bool TreeNode::operator==(const TreeNode& other) const {
    return words_ == other.words_;
}

bool TreeNode::operator!=(const TreeNode& other) const {
    return words_ != other.words_;
}

TreeNode::~TreeNode() {
    if (left_) delete left_;
    if (right_) delete right_;
}