// Copyright (c) 2012 The Khronos Group Inc.
// Permission is hereby granted, free of charge, to any person obtaining a copy of this software and /or associated documentation files (the "Materials "), to deal in the Materials without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Materials, and to permit persons to whom the Materials are furnished to do so, subject to 
// the following conditions: 
// The above copyright notice and this permission notice shall be included 
// in all copies or substantial portions of the Materials. 
// THE MATERIALS ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.


#ifndef _HIERARCHY_PRESERVATION_CHECKING_H_
#define _HIERARCHY_PRESERVATION_CHECKING_H_

#include "dae.h"
#include "dom/domCOLLADA.h"

#define PARAMETER_OFFSET (1)
#define NUM_COMMAND_LINE_PARAMETERS (3)

#include "assert.h"
#include <vector>
#include <string>
#include <algorithm>

// Prefix for notation 
// g - global variable
// i - integer
// v - vector
// str - string
// p - pointer
class NodeHPChecker
{
public:
	NodeHPChecker(daeDocument *, daeDocument *, domVisual_scene * root1, domVisual_scene * root2);
	virtual ~NodeHPChecker();

	bool IsPreserved();

protected:
	// Intermediate structures
	class TreeNode
	{
	public:
		TreeNode() : strId(""), pParent(NULL) {vChildren.clear();}

		// used when there is already a id inside!
		TreeNode(daeString strId_) : strId(strId_), pParent(NULL) {vChildren.clear();}

		// Parent node
		inline TreeNode * GetParent() {return pParent;}
		inline const TreeNode * GetParent() const {return pParent;}
		inline void SetParent(TreeNode *pParent_) {pParent = pParent_;}
		
		// must return reference!
		inline std::vector <TreeNode> & GetChildren() {return vChildren;}
		inline const std::vector <TreeNode> & GetChildren() const {return vChildren;}

		// add more children
		void AppendChildren(TreeNode *pChild); 

		// set name: 
		// PRE: Name is not null.
		inline void SetID(std::string strId_) {strId.assign(strId_);}
		inline const std::string & GetID() const {return strId;}

		// overload operators
		bool operator < (const TreeNode & pN1) const {return strId < pN1.strId;}

		// sort all children based on operator <
		void SortChildren();

	private:
		TreeNode * pParent;
		std::vector <TreeNode> vChildren;
		std::string strId;
	};

	// build a tree of domNode: strip the visual_scene and only have domNode left.
	bool InitRoots();

	// recursively loading mesh: if there is no name for node, generate one
	TreeNode *LoadNode(domNode *pNode, TreeNode *pParentNode);

	// Quick sort all strings in each children
	void SortChildren();

	// Recursively sorting nodes
	void SortChildrenR(TreeNode & pParentNode);

	// Transverse two trees to validate 
	bool TransverseTrees(NodeHPChecker::TreeNode &Node1, NodeHPChecker::TreeNode &Node2);

private:
	// forbid reference constructor
	NodeHPChecker(NodeHPChecker &) {;}

	// forbid assign operator 
	NodeHPChecker &operator = (NodeHPChecker &) {;}

	domVisual_scene *pVisualScene[2]; // two visual_scene pointers 
	daeDocument		*pDocument[2];		// two dae documents	

	TreeNode * pRoot[2];

	int giIndexNoName;

	// basic name is "HierarchyPreservation"
	std::string strBasicName;

	// name generation: id is an optional attribute. 
	void GeneratingName(TreeNode *pTNode);

};

#endif