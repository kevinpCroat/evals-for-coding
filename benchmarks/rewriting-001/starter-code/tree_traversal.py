"""
Binary Tree Traversal Operations
This module provides recursive implementations of tree traversal and analysis operations.
The challenge is to rewrite these using iterative approaches with explicit stacks.
"""

from typing import List, Optional, Callable, Any


class TreeNode:
    """A node in a binary tree."""
    def __init__(self, val: int, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        return (self.val == other.val and
                self.left == other.left and
                self.right == other.right)

    def __repr__(self):
        return f"TreeNode({self.val})"


def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """
    Perform inorder traversal of a binary tree (left, root, right).

    Current implementation: Recursive
    Target: Rewrite using iterative approach with explicit stack

    Args:
        root: Root node of the binary tree

    Returns:
        List of node values in inorder sequence
    """
    result = []

    def traverse(node: Optional[TreeNode]) -> None:
        if node is None:
            return
        traverse(node.left)
        result.append(node.val)
        traverse(node.right)

    traverse(root)
    return result


def postorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """
    Perform postorder traversal of a binary tree (left, right, root).

    Current implementation: Recursive
    Target: Rewrite using iterative approach with explicit stack

    Args:
        root: Root node of the binary tree

    Returns:
        List of node values in postorder sequence
    """
    result = []

    def traverse(node: Optional[TreeNode]) -> None:
        if node is None:
            return
        traverse(node.left)
        traverse(node.right)
        result.append(node.val)

    traverse(root)
    return result


def max_depth(root: Optional[TreeNode]) -> int:
    """
    Find the maximum depth of a binary tree.

    Current implementation: Recursive
    Target: Rewrite using iterative approach with level-order traversal or stack

    Args:
        root: Root node of the binary tree

    Returns:
        Maximum depth (number of nodes along longest path from root to leaf)
    """
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def find_path_sum(root: Optional[TreeNode], target_sum: int) -> bool:
    """
    Determine if tree has a root-to-leaf path with sum equal to target.

    Current implementation: Recursive
    Target: Rewrite using iterative approach with explicit stack tracking paths

    Args:
        root: Root node of the binary tree
        target_sum: Target sum to find

    Returns:
        True if such a path exists, False otherwise
    """
    if root is None:
        return False

    # Check if we're at a leaf node
    if root.left is None and root.right is None:
        return root.val == target_sum

    # Recursively check left and right subtrees with reduced target
    remaining = target_sum - root.val
    return (find_path_sum(root.left, remaining) or
            find_path_sum(root.right, remaining))


def collect_leaves(root: Optional[TreeNode]) -> List[int]:
    """
    Collect all leaf node values from left to right.

    Current implementation: Recursive
    Target: Rewrite using iterative approach

    Args:
        root: Root node of the binary tree

    Returns:
        List of leaf node values in left-to-right order
    """
    leaves = []

    def collect(node: Optional[TreeNode]) -> None:
        if node is None:
            return

        # If it's a leaf, collect it
        if node.left is None and node.right is None:
            leaves.append(node.val)
            return

        # Otherwise recurse
        collect(node.left)
        collect(node.right)

    collect(root)
    return leaves


def tree_map(root: Optional[TreeNode], func: Callable[[int], int]) -> Optional[TreeNode]:
    """
    Create a new tree by applying a function to each node value.

    Current implementation: Recursive
    Target: Rewrite using iterative approach

    Args:
        root: Root node of the binary tree
        func: Function to apply to each node value

    Returns:
        New tree with transformed values
    """
    if root is None:
        return None

    new_node = TreeNode(func(root.val))
    new_node.left = tree_map(root.left, func)
    new_node.right = tree_map(root.right, func)

    return new_node
