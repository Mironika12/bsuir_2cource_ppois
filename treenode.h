#pragma once
#include <iostream>
using namespace std;

class TreeNode {
public:
	TreeNode* getLeft() const;
	TreeNode* getRight() const;
	const pair<string, string>& getWords() const;
	string& getRuAdress();
	void setLeft(TreeNode*);
	void setRight(TreeNode*);
	void setWords(pair<string, string>);
	TreeNode* remove(pair<string, string>);
	TreeNode* insert(pair<string, string>);
	TreeNode* find(string);
	int nodeCount();
	TreeNode(pair<string, string> words);
	bool operator==(const TreeNode& other) const;
	bool operator!=(const TreeNode& other) const;
	~TreeNode();
private:
	TreeNode* left_, * right_;
	pair<string, string> words_;
};
