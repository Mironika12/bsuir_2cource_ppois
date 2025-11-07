#pragma once
#include <iostream>
#include "treenode.h"
using namespace std;

class Dict {
public:
	Dict& operator +=(const pair<string, string>&);
	Dict& operator -=(const pair<string, string>&);
	string operator[](const string&) const;
	string& operator[](const string&);
	bool empty();
	TreeNode* getRoot();
	Dict();
	Dict(pair<string, string>);
	~Dict();
	Dict(const Dict& other);
	Dict& operator=(const Dict& other);
	friend std::ostream& operator<<(std::ostream& os, const Dict& dict);
	friend std::istream& operator>>(std::istream& is, Dict& dict);
	void outputDict(std::ostream& os, TreeNode* node) const;
	TreeNode* inputDict(std::istream& is);
private:
	TreeNode* root;
};
