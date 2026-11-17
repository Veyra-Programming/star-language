"""
Star Language Abstract Syntax Tree (AST) Nodes
Authoritative Reference: STAR_SPEC.md (Section 5)
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple, Any
from star_engine.tokens import SourceLocation, TokenType


@dataclass
class ASTNode:
    location: SourceLocation


# Expressions
@dataclass
class ExpressionNode(ASTNode):
    pass


@dataclass
class LiteralNode(ExpressionNode):
    value: Any
    literal_type: str  # "Integer", "Decimal", "Text", "Boolean", "Null"


@dataclass
class IdentifierNode(ExpressionNode):
    name: str


@dataclass
class SelfNode(ExpressionNode):
    pass


@dataclass
class BinaryOpNode(ExpressionNode):
    left: ExpressionNode
    operator: TokenType
    right: ExpressionNode


@dataclass
class UnaryOpNode(ExpressionNode):
    operator: TokenType
    operand: ExpressionNode


@dataclass
class CallArg:
    name: Optional[str]  # e.g. 'name' in User(name = "Alex")
    value: ExpressionNode


@dataclass
class CallNode(ExpressionNode):
    callee: ExpressionNode
    arguments: List[CallArg]


@dataclass
class IndexNode(ExpressionNode):
    target: ExpressionNode
    index: ExpressionNode


@dataclass
class MemberAccessNode(ExpressionNode):
    target: ExpressionNode
    member: str


@dataclass
class ListNode(ExpressionNode):
    elements: List[ExpressionNode]


@dataclass
class MapNode(ExpressionNode):
    entries: List[Tuple[ExpressionNode, ExpressionNode]]


# Statements
@dataclass
class StatementNode(ASTNode):
    pass


@dataclass
class ProgramNode(ASTNode):
    statements: List[StatementNode]


@dataclass
class AppNode(StatementNode):
    name: str
    body: List[StatementNode]


@dataclass
class PropertyDeclNode(StatementNode):
    name: str
    type_annotation: Optional[str]
    initializer: Optional[ExpressionNode]


@dataclass
class FunctionDefNode(StatementNode):
    name: str
    parameters: List[str]
    body: List[StatementNode]


@dataclass
class ClassDeclNode(StatementNode):
    name: str
    properties: List[PropertyDeclNode]
    methods: List[FunctionDefNode]
    is_durable: bool = False


@dataclass
class StateDeclNode(StatementNode):
    name: str
    type_annotation: Optional[str]
    initializer: Optional[ExpressionNode]


@dataclass
class ComputedDeclNode(StatementNode):
    name: str
    expression: ExpressionNode


@dataclass
class WatchDeclNode(StatementNode):
    target_state: str
    handler: StatementNode  # FunctionDefNode or ExpressionStmtNode (closure)


@dataclass
class EventDeclNode(StatementNode):
    name: str
    parameters: List[str]


@dataclass
class RenderDeclNode(StatementNode):
    body: List[StatementNode]


@dataclass
class ComponentDeclNode(StatementNode):
    name: str
    states: List[StateDeclNode]
    computeds: List[ComputedDeclNode]
    watchers: List[WatchDeclNode]
    events: List[EventDeclNode]
    methods: List[FunctionDefNode]
    render_decl: Optional[RenderDeclNode]


@dataclass
class UseStmtNode(StatementNode):
    module_name: str
    is_file: bool


@dataclass
class VarDeclNode(StatementNode):
    name: str
    type_annotation: Optional[str]
    initializer: Optional[ExpressionNode]


@dataclass
class ConstDeclNode(StatementNode):
    name: str
    type_annotation: Optional[str]
    initializer: ExpressionNode


@dataclass
class AssignNode(StatementNode):
    target: ExpressionNode  # IdentifierNode, IndexNode, MemberAccessNode, or SelfNode
    value: ExpressionNode


@dataclass
class ShowNode(StatementNode):
    expression: ExpressionNode


@dataclass
class ReturnNode(StatementNode):
    expression: Optional[ExpressionNode]


@dataclass
class BreakNode(StatementNode):
    pass


@dataclass
class ContinueNode(StatementNode):
    pass


@dataclass
class IfNode(StatementNode):
    condition: ExpressionNode
    then_body: List[StatementNode]
    elif_branches: List[Tuple[ExpressionNode, List[StatementNode]]]
    else_body: Optional[List[StatementNode]]


@dataclass
class WhileNode(StatementNode):
    condition: ExpressionNode
    body: List[StatementNode]


@dataclass
class RepeatNode(StatementNode):
    count: ExpressionNode
    body: List[StatementNode]


@dataclass
class ForNode(StatementNode):
    variable_name: str
    iterable: ExpressionNode
    body: List[StatementNode]


@dataclass
class TryCatchNode(StatementNode):
    try_body: List[StatementNode]
    error_variable: str
    catch_body: List[StatementNode]


@dataclass
class ExpressionStmtNode(StatementNode):
    expression: ExpressionNode


@dataclass
class EnsureNode(StatementNode):
    condition: ExpressionNode
    message: Optional[ExpressionNode] = None


@dataclass
class RecordDeclNode(StatementNode):
    name: str
    property_names: List[str]
