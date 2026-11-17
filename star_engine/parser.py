"""
Star Language Parser
Authoritative Reference: STAR_SPEC.md (Section 4 & Section 5)
"""

from typing import List, Optional, Tuple, Any, Any
from star_engine.tokens import TokenType, Token, SourceLocation, KEYWORDS
from star_engine.errors import StarSyntaxError
from star_engine.ast_nodes import (
    ProgramNode, StatementNode, ExpressionNode,
    AppNode, ClassDeclNode, PropertyDeclNode, UseStmtNode,
    FunctionDefNode, VarDeclNode, ConstDeclNode,
    AssignNode, ShowNode, ReturnNode, BreakNode, ContinueNode,
    IfNode, WhileNode, RepeatNode, ForNode, TryCatchNode, ExpressionStmtNode, EnsureNode,
    LiteralNode, IdentifierNode, SelfNode, BinaryOpNode, UnaryOpNode,
    CallNode, CallArg, IndexNode, MemberAccessNode, ListNode, MapNode,
    ComponentDeclNode, StateDeclNode, ComputedDeclNode, WatchDeclNode, EventDeclNode, RenderDeclNode
)


class Parser:
    def __init__(self, tokens: List[Token], source_code: str = "", filename: str = "<stdin>"):
        self.tokens = tokens
        self.source_code = source_code
        self.filename = filename
        self.current = 0

    def parse(self) -> ProgramNode:
        statements: List[StatementNode] = []
        self._skip_newlines()

        first_loc = self._peek().location
        while not self._is_at_end():
            stmt = self._declaration()
            if stmt:
                statements.append(stmt)
            self._skip_newlines()

        return ProgramNode(location=first_loc, statements=statements)

    # ---------------- Helper Methods ----------------

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _peek_next(self) -> Token:
        if self.current + 1 < len(self.tokens):
            return self.tokens[self.current + 1]
        return self._peek()

    def _peek_ahead_non_newline(self) -> Token:
        idx = self.current
        while idx < len(self.tokens) and self.tokens[idx].type == TokenType.NEWLINE:
            idx += 1
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self._peek()

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _match(self, *types: TokenType) -> bool:
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str, suggestion: Optional[str] = None) -> Token:
        if self._check(token_type):
            return self._advance()
        tok = self._peek()
        raise StarSyntaxError(message, tok.location, suggestion, self.source_code)

    def _skip_newlines(self):
        while self._match(TokenType.NEWLINE, TokenType.SEMICOLON):
            pass

    # ---------------- Statements & Declarations ----------------

    def _declaration(self) -> Optional[StatementNode]:
        self._skip_newlines()
        if self._is_at_end():
            return None

        if self._match(TokenType.APP):
            return self._app_declaration()
        if self._match(TokenType.CLASS):
            return self._class_declaration()
        if self._match(TokenType.COMPONENT):
            return self._component_declaration()
        if self._match(TokenType.USE):
            return self._use_statement()
        if self._match(TokenType.FUNCTION, TokenType.DEFINE):
            return self._function_declaration()
        if self._check(TokenType.TO) and self._peek_next().type == TokenType.IDENTIFIER:
            self._advance()
            return self._function_declaration()
        if self._match(TokenType.VARIABLE):
            return self._variable_declaration()
        if self._match(TokenType.CONSTANT):
            return self._constant_declaration()
        if self._match(TokenType.DURABLE):
            self._consume(TokenType.RECORD, "Expected 'record' after 'durable'.")
            return self._durable_record_declaration()

        return self._statement()

    def _durable_record_declaration(self) -> ClassDeclNode:
        rec_tok = self._previous()
        name_tok = self._consume(TokenType.IDENTIFIER, "Expected record name after 'durable record'.")
        self._match(TokenType.COLON)
        self._skip_newlines()
        fields: List[PropertyDeclNode] = []
        while not self._check(TokenType.END) and not self._is_at_end():
            self._skip_newlines()
            if self._check(TokenType.END) or self._is_at_end():
                break
            prop_tok = self._consume(TokenType.IDENTIFIER, "Expected field name in durable record.")
            prop_type = None
            if self._match(TokenType.COLON):
                if self._check(TokenType.IDENTIFIER):
                    prop_type = self._advance().lexeme
            default_val = None
            if self._match(TokenType.EQUAL):
                default_val = self._expression()
            fields.append(PropertyDeclNode(location=prop_tok.location, name=prop_tok.lexeme, type_annotation=prop_type, initializer=default_val))
            self._skip_newlines()
        self._consume(TokenType.END, f"Expected 'end' to close durable record '{name_tok.lexeme}'.")
        return ClassDeclNode(location=rec_tok.location, name=name_tok.lexeme, properties=fields, methods=[], is_durable=True)

    def _app_declaration(self) -> AppNode:
        app_token = self._previous()
        name_token = self._consume(TokenType.IDENTIFIER, "Expected application name after 'app'.", "Provide a name for the app (e.g. `app MyApp`).")
        self._match(TokenType.COLON)
        self._skip_newlines()

        body = self._block_until(TokenType.END)
        self._consume(TokenType.END, f"Expected 'end' to close app '{name_token.lexeme}'.", "Add 'end' at the end of the app block.")
        return AppNode(location=app_token.location, name=name_token.lexeme, body=body)

    def _component_declaration(self) -> ComponentDeclNode:
        comp_token = self._previous()
        name_token = self._consume(TokenType.IDENTIFIER, "Expected component name after 'component'.", "Provide a valid component name (e.g. `component Counter`).")
        self._match(TokenType.COLON)
        self._skip_newlines()

        states: List[StateDeclNode] = []
        computeds: List[ComputedDeclNode] = []
        watchers: List[WatchDeclNode] = []
        events: List[EventDeclNode] = []
        methods: List[FunctionDefNode] = []
        render_decl: Optional[RenderDeclNode] = None

        while not self._check(TokenType.END) and not self._is_at_end():
            self._skip_newlines()
            if self._check(TokenType.END) or self._is_at_end():
                break

            if self._match(TokenType.STATE, TokenType.REMEMBER):
                st_tok = self._previous()
                s_name = self._consume(TokenType.IDENTIFIER, "Expected state variable name.").lexeme
                s_type = None
                if self._match(TokenType.COLON):
                    s_type = self._consume(TokenType.IDENTIFIER, "Expected type name after ':'.", "Specify a valid type.").lexeme
                s_init = None
                if self._match(TokenType.EQUAL, TokenType.AS, TokenType.TO):
                    s_init = self._expression()
                states.append(StateDeclNode(location=st_tok.location, name=s_name, type_annotation=s_type, initializer=s_init))

            elif self._match(TokenType.COMPUTED):
                comp_tok = self._previous()
                c_name = self._consume(TokenType.IDENTIFIER, "Expected computed property name after 'computed'.").lexeme
                self._consume(TokenType.EQUAL, "Expected '=' after computed property name.")
                c_expr = self._expression()
                computeds.append(ComputedDeclNode(location=comp_tok.location, name=c_name, expression=c_expr))

            elif self._match(TokenType.WATCH):
                w_tok = self._previous()
                target_state = self._consume(TokenType.IDENTIFIER, "Expected state variable name after 'watch'.").lexeme
                self._skip_newlines()
                if self._match(TokenType.FUNCTION, TokenType.DEFINE):
                    fn_tok = self._previous()
                    fn_name = ""
                    if self._check(TokenType.IDENTIFIER):
                        fn_name = self._advance().lexeme
                    self._consume(TokenType.LPAREN, "Expected '(' after function.")
                    params = []
                    if not self._check(TokenType.RPAREN):
                        params.append(self._consume(TokenType.IDENTIFIER, "Expected parameter name.").lexeme)
                        while self._match(TokenType.COMMA):
                            params.append(self._consume(TokenType.IDENTIFIER, "Expected parameter name after ','.").lexeme)
                    self._consume(TokenType.RPAREN, "Expected ')' after parameter list.")
                    self._match(TokenType.COLON)
                    self._skip_newlines()
                    body = self._block_until(TokenType.END)
                    self._consume(TokenType.END, "Expected 'end' to close function.")
                    handler = FunctionDefNode(location=fn_tok.location, name=fn_name, parameters=params, body=body)
                else:
                    body = self._block_until(TokenType.END)
                    self._consume(TokenType.END, f"Expected 'end' to close watch on '{target_state}'.")
                    handler = FunctionDefNode(location=w_tok.location, name="", parameters=["new_val", "old_val"], body=body)
                watchers.append(WatchDeclNode(location=w_tok.location, target_state=target_state, handler=handler))

            elif self._match(TokenType.EVENT):
                ev_tok = self._previous()
                ev_name = self._consume(TokenType.IDENTIFIER, "Expected event name after 'event'.").lexeme
                ev_params = []
                if self._match(TokenType.LPAREN):
                    if not self._check(TokenType.RPAREN):
                        ev_params.append(self._consume(TokenType.IDENTIFIER, "Expected parameter name.").lexeme)
                        while self._match(TokenType.COMMA):
                            ev_params.append(self._consume(TokenType.IDENTIFIER, "Expected parameter name after ','.").lexeme)
                    self._consume(TokenType.RPAREN, "Expected ')' after event parameter list.")
                events.append(EventDeclNode(location=ev_tok.location, name=ev_name, parameters=ev_params))

            elif self._match(TokenType.FUNCTION, TokenType.DEFINE):
                fn = self._function_declaration()
                methods.append(fn)

            elif self._check(TokenType.TO) and self._peek_next().type == TokenType.IDENTIFIER:
                self._advance()
                fn = self._function_declaration()
                methods.append(fn)

            elif self._match(TokenType.RENDER):
                r_tok = self._previous()
                self._match(TokenType.COLON)
                self._skip_newlines()
                r_body = self._block_until(TokenType.END)
                self._consume(TokenType.END, f"Expected 'end' to close render block in component '{name_token.lexeme}'.")
                render_decl = RenderDeclNode(location=r_tok.location, body=r_body)

            else:
                tok = self._peek()
                raise StarSyntaxError(
                    f"Unexpected declaration '{tok.lexeme or tok.type.name}' inside component '{name_token.lexeme}'.",
                    tok.location,
                    "Components may contain 'state', 'computed', 'watch', 'event', 'function', and 'render' blocks.",
                    self.source_code
                )
            self._skip_newlines()

        self._consume(TokenType.END, f"Expected 'end' to close component '{name_token.lexeme}'.", "Add 'end' at the end of the component block.")
        return ComponentDeclNode(
            location=comp_token.location,
            name=name_token.lexeme,
            states=states,
            computeds=computeds,
            watchers=watchers,
            events=events,
            methods=methods,
            render_decl=render_decl
        )

    def _class_declaration(self) -> ClassDeclNode:
        class_token = self._previous()
        name_token = self._consume(TokenType.IDENTIFIER, "Expected class name after 'class'.", "Provide a valid class name (e.g. `class User`).")
        self._match(TokenType.COLON)
        self._skip_newlines()

        properties: List[PropertyDeclNode] = []
        methods: List[FunctionDefNode] = []

        while not self._check(TokenType.END) and not self._is_at_end():
            self._skip_newlines()
            if self._check(TokenType.END) or self._is_at_end():
                break

            if self._match(TokenType.PROPERTY):
                prop_tok = self._previous()
                p_name_tok = self._consume(TokenType.IDENTIFIER, "Expected property name after 'property'.")
                p_type = None
                if self._match(TokenType.COLON):
                    t_tok = self._consume(TokenType.IDENTIFIER, "Expected type name after ':'.")
                    p_type = t_tok.lexeme
                p_init = None
                if self._match(TokenType.EQUAL):
                    p_init = self._expression()
                properties.append(PropertyDeclNode(location=prop_tok.location, name=p_name_tok.lexeme, type_annotation=p_type, initializer=p_init))
            elif self._match(TokenType.FUNCTION, TokenType.DEFINE):
                fn = self._function_declaration()
                methods.append(fn)
            elif self._check(TokenType.TO) and self._peek_next().type == TokenType.IDENTIFIER:
                self._advance()
                fn = self._function_declaration()
                methods.append(fn)
            else:
                tok = self._peek()
                raise StarSyntaxError(
                    f"Unexpected declaration '{tok.lexeme or tok.type.name}' inside class '{name_token.lexeme}'.",
                    tok.location,
                    "Classes may only contain 'property' and 'function' definitions.",
                    self.source_code
                )
            self._skip_newlines()

        self._consume(TokenType.END, f"Expected 'end' to close class '{name_token.lexeme}'.", "Add 'end' at the end of the class block.")
        return ClassDeclNode(location=class_token.location, name=name_token.lexeme, properties=properties, methods=methods)

    def _use_statement(self) -> UseStmtNode:
        use_tok = self._previous()
        if self._match(TokenType.IDENTIFIER):
            mod_name = self._previous().lexeme
            return UseStmtNode(location=use_tok.location, module_name=mod_name, is_file=False)
        elif self._match(TokenType.TEXT):
            file_name = self._previous().value
            return UseStmtNode(location=use_tok.location, module_name=file_name, is_file=True)
        else:
            tok = self._peek()
            raise StarSyntaxError(
                "Expected module name or file path after 'use'.",
                tok.location,
                "Example: `use Math` or `use \"utils.star\"`.",
                self.source_code
            )

    def _function_declaration(self) -> FunctionDefNode:
        func_token = self._previous()
        name_token = self._consume(TokenType.IDENTIFIER, "Expected function name.", "Provide a valid function name (e.g. `define calculate()`).")
        
        self._consume(TokenType.LPAREN, "Expected '(' after function name.")
        params: List[str] = []
        if not self._check(TokenType.RPAREN):
            param_tok = self._consume(TokenType.IDENTIFIER, "Expected parameter name.")
            params.append(param_tok.lexeme)
            while self._match(TokenType.COMMA):
                param_tok = self._consume(TokenType.IDENTIFIER, "Expected parameter name after ','.")
                params.append(param_tok.lexeme)
        self._consume(TokenType.RPAREN, "Expected ')' after parameter list.")
        self._match(TokenType.COLON)
        self._skip_newlines()

        body = self._block_until(TokenType.END)
        self._consume(TokenType.END, f"Expected 'end' to close function '{name_token.lexeme}'.", "Add 'end' to close the function block.")
        return FunctionDefNode(location=func_token.location, name=name_token.lexeme, parameters=params, body=body)

    def _variable_declaration(self) -> VarDeclNode:
        var_token = self._previous()
        name_tok = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'variable'.")
        
        type_annotation = None
        if self._match(TokenType.COLON):
            type_tok = self._consume(TokenType.IDENTIFIER, "Expected type name after ':'.", "Specify a valid type such as Text, Integer, Decimal, Boolean, List, Map.")
            type_annotation = type_tok.lexeme

        initializer = None
        if self._match(TokenType.EQUAL):
            initializer = self._expression()

        return VarDeclNode(location=var_token.location, name=name_tok.lexeme, type_annotation=type_annotation, initializer=initializer)

    def _constant_declaration(self) -> ConstDeclNode:
        const_token = self._previous()
        name_tok = self._consume(TokenType.IDENTIFIER, "Expected constant name after 'constant'.")

        type_annotation = None
        if self._match(TokenType.COLON):
            type_tok = self._consume(TokenType.IDENTIFIER, "Expected type name after ':'.")
            type_annotation = type_tok.lexeme

        self._consume(TokenType.EQUAL, "Constant declaration must be initialized with '='.", "Provide an initial value (e.g. `constant MAX = 100`).")
        initializer = self._expression()

        return ConstDeclNode(location=const_token.location, name=name_tok.lexeme, type_annotation=type_annotation, initializer=initializer)

    def _statement(self) -> StatementNode:
        if self._match(TokenType.SHOW, TokenType.SAY):
            return self._show_statement()
        if self._match(TokenType.RETURN):
            return self._return_statement()
        if self._match(TokenType.GIVE):
            self._consume(TokenType.BACK, "Expected 'back' after 'give' (e.g. `give back x`).")
            return self._return_statement()
        if self._match(TokenType.BREAK):
            return BreakNode(location=self._previous().location)
        if self._match(TokenType.CONTINUE):
            return ContinueNode(location=self._previous().location)
        if self._match(TokenType.IF, TokenType.WHENEVER):
            return self._if_statement()
        if self._match(TokenType.UNLESS):
            return self._unless_statement()
        if self._match(TokenType.WHILE):
            return self._while_statement()
        if self._match(TokenType.UNTIL):
            return self._until_statement()
        if self._match(TokenType.FOREVER):
            return self._forever_statement()
        if self._match(TokenType.REPEAT):
            return self._repeat_statement()
        if self._match(TokenType.FOR):
            return self._for_statement()
        if self._match(TokenType.TRY):
            return self._try_catch_statement()
        if self._match(TokenType.SET):
            return self._set_statement()
        if self._match(TokenType.LET):
            return self._let_statement()
        if self._match(TokenType.REMEMBER):
            return self._remember_statement()
        if self._match(TokenType.INCREASE):
            return self._increase_statement()
        if self._match(TokenType.DECREASE):
            return self._decrease_statement()
        if self._match(TokenType.ENSURE):
            return self._ensure_statement()

        return self._assignment_or_expression_statement()

    def _show_statement(self) -> ShowNode:
        show_tok = self._previous()
        expr = self._expression()
        return ShowNode(location=show_tok.location, expression=expr)

    def _return_statement(self) -> ReturnNode:
        ret_tok = self._previous()
        expr = None
        if not self._check(TokenType.NEWLINE) and not self._check(TokenType.SEMICOLON) and not self._check(TokenType.END) and not self._is_at_end():
            expr = self._expression()
        return ReturnNode(location=ret_tok.location, expression=expr)

    def _if_statement(self) -> IfNode:
        if_tok = self._previous()
        cond = self._expression()
        self._match(TokenType.COLON)
        self._skip_newlines()

        then_body = self._block_until(TokenType.ELSE, TokenType.OTHERWISE, TokenType.END)
        elif_branches: List[Tuple[ExpressionNode, List[StatementNode]]] = []
        else_body = None

        while self._match(TokenType.ELSE, TokenType.OTHERWISE):
            if self._match(TokenType.IF, TokenType.WHENEVER):
                elif_cond = self._expression()
                self._match(TokenType.COLON)
                self._skip_newlines()
                elif_body = self._block_until(TokenType.ELSE, TokenType.OTHERWISE, TokenType.END)
                elif_branches.append((elif_cond, elif_body))
            else:
                self._match(TokenType.COLON)
                self._skip_newlines()
                else_body = self._block_until(TokenType.END)
                break

        self._consume(TokenType.END, "Expected 'end' to close conditional statement.", "Add 'end' at the end of the block.")
        return IfNode(location=if_tok.location, condition=cond, then_body=then_body, elif_branches=elif_branches, else_body=else_body)

    def _unless_statement(self) -> IfNode:
        unless_tok = self._previous()
        cond = self._expression()
        self._match(TokenType.COLON)
        self._skip_newlines()
        not_cond = UnaryOpNode(location=cond.location, operator=TokenType.NOT, operand=cond)
        then_body = self._block_until(TokenType.ELSE, TokenType.OTHERWISE, TokenType.END)
        elif_branches: List[Tuple[ExpressionNode, List[StatementNode]]] = []
        else_body = None

        while self._match(TokenType.ELSE, TokenType.OTHERWISE):
            if self._match(TokenType.IF, TokenType.WHENEVER):
                elif_cond = self._expression()
                self._match(TokenType.COLON)
                self._skip_newlines()
                elif_body = self._block_until(TokenType.ELSE, TokenType.OTHERWISE, TokenType.END)
                elif_branches.append((elif_cond, elif_body))
            else:
                self._match(TokenType.COLON)
                self._skip_newlines()
                else_body = self._block_until(TokenType.END)
                break

        self._consume(TokenType.END, "Expected 'end' to close 'unless' statement.", "Add 'end' at the end of the unless block.")
        return IfNode(location=unless_tok.location, condition=not_cond, then_body=then_body, elif_branches=elif_branches, else_body=else_body)

    def _while_statement(self) -> WhileNode:
        while_tok = self._previous()
        cond = self._expression()
        self._match(TokenType.COLON)
        self._skip_newlines()
        body = self._block_until(TokenType.END)
        self._consume(TokenType.END, "Expected 'end' to close 'while' loop.")
        return WhileNode(location=while_tok.location, condition=cond, body=body)

    def _until_statement(self) -> WhileNode:
        until_tok = self._previous()
        cond = self._expression()
        self._match(TokenType.COLON)
        self._skip_newlines()
        not_cond = UnaryOpNode(location=cond.location, operator=TokenType.NOT, operand=cond)
        body = self._block_until(TokenType.END)
        self._consume(TokenType.END, "Expected 'end' to close 'until' loop.")
        return WhileNode(location=until_tok.location, condition=not_cond, body=body)

    def _forever_statement(self) -> WhileNode:
        forever_tok = self._previous()
        self._match(TokenType.COLON)
        self._skip_newlines()
        true_node = LiteralNode(location=forever_tok.location, value=True, literal_type="Boolean")
        body = self._block_until(TokenType.END)
        self._consume(TokenType.END, "Expected 'end' to close 'forever' loop.")
        return WhileNode(location=forever_tok.location, condition=true_node, body=body)

    def _repeat_statement(self) -> RepeatNode:
        repeat_tok = self._previous()
        count = self._expression()
        self._match(TokenType.TIMES)
        self._match(TokenType.COLON)
        self._skip_newlines()
        body = self._block_until(TokenType.END)
        self._consume(TokenType.END, "Expected 'end' to close 'repeat' loop.")
        return RepeatNode(location=repeat_tok.location, count=count, body=body)

    def _for_statement(self) -> ForNode:
        for_tok = self._previous()
        self._match(TokenType.EACH)
        var_tok = self._consume(TokenType.IDENTIFIER, "Expected variable name in for-loop.")
        self._consume(TokenType.IN, "Expected 'in' after variable name in for-loop.", "Use `for each item in items` syntax.")
        iterable = self._expression()
        self._match(TokenType.COLON)
        self._skip_newlines()
        body = self._block_until(TokenType.END)
        self._consume(TokenType.END, "Expected 'end' to close 'for' loop.")
        return ForNode(location=for_tok.location, variable_name=var_tok.lexeme, iterable=iterable, body=body)

    def _try_catch_statement(self) -> TryCatchNode:
        try_tok = self._previous()
        self._match(TokenType.COLON)
        self._skip_newlines()
        try_body = self._block_until(TokenType.CATCH, TokenType.RECOVER)
        if not self._match(TokenType.CATCH, TokenType.RECOVER):
            raise StarSyntaxError("Expected 'catch' or 'recover' after 'try' block.", self._peek().location, "Example: `try: ... recover as err: ... end`", self.source_code)
        
        self._match(TokenType.AS)
        err_var_name = "err"
        if self._check(TokenType.IDENTIFIER):
            err_var_name = self._advance().lexeme
        self._match(TokenType.COLON)
        self._skip_newlines()
        catch_body = self._block_until(TokenType.END)
        self._consume(TokenType.END, "Expected 'end' to close 'try/recover' statement.")
        return TryCatchNode(location=try_tok.location, try_body=try_body, error_variable=err_var_name, catch_body=catch_body)

    def _set_statement(self) -> AssignNode:
        set_tok = self._previous()
        target = self._postfix()
        if not isinstance(target, (IdentifierNode, IndexNode, MemberAccessNode, SelfNode)):
            raise StarSyntaxError("Invalid target in 'set' statement.", target.location, "Target must be a variable, property, or index.", self.source_code)
        self._consume(TokenType.TO, "Expected 'to' in 'set <name> to <value>' statement.", "Example: `set count to 0`.")
        value = self._expression()
        return AssignNode(location=set_tok.location, target=target, value=value)

    def _let_statement(self) -> VarDeclNode:
        let_tok = self._previous()
        name_tok = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'let'.")
        type_annotation = None
        if self._match(TokenType.COLON):
            type_tok = self._consume(TokenType.IDENTIFIER, "Expected type name after ':'.")
            type_annotation = type_tok.lexeme
        if not self._match(TokenType.BE, TokenType.EQUAL):
            raise StarSyntaxError("Expected 'be' or '=' after variable name in 'let' statement.", self._peek().location, "Example: `let count be 10` or `let count = 10`.", self.source_code)
        initializer = self._expression()
        return VarDeclNode(location=let_tok.location, name=name_tok.lexeme, type_annotation=type_annotation, initializer=initializer)

    def _remember_statement(self) -> VarDeclNode:
        rem_tok = self._previous()
        name_tok = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'remember'.")
        type_annotation = None
        if self._match(TokenType.COLON):
            type_tok = self._consume(TokenType.IDENTIFIER, "Expected type name after ':'.")
            type_annotation = type_tok.lexeme
        if not self._match(TokenType.AS, TokenType.EQUAL, TokenType.TO):
            raise StarSyntaxError("Expected 'as' or '=' after variable name in 'remember' statement.", self._peek().location, "Example: `remember key as \"abc\"`.", self.source_code)
        initializer = self._expression()
        return VarDeclNode(location=rem_tok.location, name=name_tok.lexeme, type_annotation=type_annotation, initializer=initializer)

    def _increase_statement(self) -> AssignNode:
        inc_tok = self._previous()
        target = self._postfix()
        if not isinstance(target, (IdentifierNode, IndexNode, MemberAccessNode, SelfNode)):
            raise StarSyntaxError("Invalid target in 'increase' statement.", target.location, "Target must be a variable, property, or index.", self.source_code)
        amount = None
        if self._match(TokenType.BY):
            amount = self._expression()
        else:
            amount = LiteralNode(location=inc_tok.location, value=1, literal_type="Integer")
        plus_expr = BinaryOpNode(location=inc_tok.location, left=target, operator=TokenType.PLUS, right=amount)
        return AssignNode(location=inc_tok.location, target=target, value=plus_expr)

    def _decrease_statement(self) -> AssignNode:
        dec_tok = self._previous()
        target = self._postfix()
        if not isinstance(target, (IdentifierNode, IndexNode, MemberAccessNode, SelfNode)):
            raise StarSyntaxError("Invalid target in 'decrease' statement.", target.location, "Target must be a variable, property, or index.", self.source_code)
        amount = None
        if self._match(TokenType.BY):
            amount = self._expression()
        else:
            amount = LiteralNode(location=dec_tok.location, value=1, literal_type="Integer")
        minus_expr = BinaryOpNode(location=dec_tok.location, left=target, operator=TokenType.MINUS, right=amount)
        return AssignNode(location=dec_tok.location, target=target, value=minus_expr)

    def _ensure_statement(self) -> EnsureNode:
        ens_tok = self._previous()
        cond = self._expression()
        msg = None
        if self._match(TokenType.OTHERWISE):
            msg = self._expression()
        return EnsureNode(location=ens_tok.location, condition=cond, message=msg)

    def _block_until(self, *end_tokens: TokenType) -> List[StatementNode]:
        statements: List[StatementNode] = []
        while not self._is_at_end() and not any(self._check(t) for t in end_tokens):
            self._skip_newlines()
            if any(self._check(t) for t in end_tokens) or self._is_at_end():
                break
            stmt = self._declaration()
            if stmt:
                statements.append(stmt)
            self._skip_newlines()
        return statements

    def _assignment_or_expression_statement(self) -> StatementNode:
        expr = self._expression()

        if self._match(TokenType.EQUAL):
            eq_tok = self._previous()
            if not isinstance(expr, (IdentifierNode, IndexNode, MemberAccessNode)):
                raise StarSyntaxError("Invalid assignment target.", expr.location, "Assignments must target a variable, property, or index.", self.source_code)
            value = self._expression()
            return AssignNode(location=eq_tok.location, target=expr, value=value)

        return ExpressionStmtNode(location=expr.location, expression=expr)

    # ---------------- Expression Parsing ----------------

    def _expression(self) -> ExpressionNode:
        return self._pipe()

    def _pipe(self) -> ExpressionNode:
        expr = self._logical_or()
        while True:
            if self._peek_ahead_non_newline().type == TokenType.PIPE_GREATER:
                self._skip_newlines()
                pipe_tok = self._advance()
                self._skip_newlines()
                right = self._logical_or()
                expr = self._desugar_pipe(pipe_tok, expr, right)
            else:
                break
        return expr

    def _desugar_pipe(self, pipe_tok: Any, left: ExpressionNode, right: ExpressionNode) -> ExpressionNode:
        if isinstance(right, CallNode):
            found_placeholder = False
            new_args = []
            for arg in right.arguments:
                if isinstance(arg.value, IdentifierNode) and arg.value.name == "_":
                    new_args.append(CallArg(name=arg.name, value=left))
                    found_placeholder = True
                else:
                    new_args.append(arg)
            if not found_placeholder:
                new_args.insert(0, CallArg(name=None, value=left))
            return CallNode(location=pipe_tok.location, callee=right.callee, arguments=new_args)
        elif isinstance(right, (IdentifierNode, MemberAccessNode)):
            return CallNode(location=pipe_tok.location, callee=right, arguments=[CallArg(name=None, value=left)])
        else:
            return CallNode(location=pipe_tok.location, callee=right, arguments=[CallArg(name=None, value=left)])

    def _logical_or(self) -> ExpressionNode:
        expr = self._logical_and()
        while self._match(TokenType.OR):
            op = self._previous()
            right = self._logical_and()
            expr = BinaryOpNode(location=op.location, left=expr, operator=op.type, right=right)
        return expr

    def _logical_and(self) -> ExpressionNode:
        expr = self._equality()
        while self._match(TokenType.AND):
            op = self._previous()
            right = self._equality()
            expr = BinaryOpNode(location=op.location, left=expr, operator=op.type, right=right)
        return expr

    def _equality(self) -> ExpressionNode:
        expr = self._relational()
        while True:
            if self._match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
                op = self._previous()
                right = self._relational()
                expr = BinaryOpNode(location=op.location, left=expr, operator=op.type, right=right)
            elif self._match(TokenType.IS):
                is_tok = self._previous()
                if self._match(TokenType.NOT):
                    if self._check(TokenType.IDENTIFIER) and self._peek().lexeme == "equal":
                        self._advance()
                        self._match(TokenType.TO)
                    right = self._relational()
                    expr = BinaryOpNode(location=is_tok.location, left=expr, operator=TokenType.BANG_EQUAL, right=right)
                elif self._check(TokenType.IDENTIFIER) and self._peek().lexeme == "equal":
                    self._advance()
                    self._match(TokenType.TO)
                    right = self._relational()
                    expr = BinaryOpNode(location=is_tok.location, left=expr, operator=TokenType.EQUAL_EQUAL, right=right)
                elif self._check(TokenType.IDENTIFIER) and self._peek().lexeme == "greater":
                    self._advance()
                    if self._check(TokenType.IDENTIFIER) and self._peek().lexeme == "than":
                        self._advance()
                    if self._match(TokenType.OR) and self._check(TokenType.IDENTIFIER) and self._peek().lexeme == "equal":
                        self._advance()
                        self._match(TokenType.TO)
                        right = self._relational()
                        expr = BinaryOpNode(location=is_tok.location, left=expr, operator=TokenType.GREATER_EQUAL, right=right)
                    else:
                        right = self._relational()
                        expr = BinaryOpNode(location=is_tok.location, left=expr, operator=TokenType.GREATER, right=right)
                elif self._check(TokenType.IDENTIFIER) and self._peek().lexeme == "less":
                    self._advance()
                    if self._check(TokenType.IDENTIFIER) and self._peek().lexeme == "than":
                        self._advance()
                    if self._match(TokenType.OR) and self._check(TokenType.IDENTIFIER) and self._peek().lexeme == "equal":
                        self._advance()
                        self._match(TokenType.TO)
                        right = self._relational()
                        expr = BinaryOpNode(location=is_tok.location, left=expr, operator=TokenType.LESS_EQUAL, right=right)
                    else:
                        right = self._relational()
                        expr = BinaryOpNode(location=is_tok.location, left=expr, operator=TokenType.LESS, right=right)
                elif self._check(TokenType.IDENTIFIER) and self._peek().lexeme == "at":
                    self._advance()
                    if self._check(TokenType.IDENTIFIER) and self._peek().lexeme == "least":
                        self._advance()
                        right = self._relational()
                        expr = BinaryOpNode(location=is_tok.location, left=expr, operator=TokenType.GREATER_EQUAL, right=right)
                    elif self._check(TokenType.IDENTIFIER) and self._peek().lexeme == "most":
                        self._advance()
                        right = self._relational()
                        expr = BinaryOpNode(location=is_tok.location, left=expr, operator=TokenType.LESS_EQUAL, right=right)
                    else:
                        raise StarSyntaxError("Expected 'least' or 'most' after 'is at'.", self._peek().location, "Example: `x is at least 10`", self.source_code)
                else:
                    right = self._relational()
                    expr = BinaryOpNode(location=is_tok.location, left=expr, operator=TokenType.EQUAL_EQUAL, right=right)
            else:
                break
        return expr

    def _relational(self) -> ExpressionNode:
        expr = self._additive()
        while self._match(TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL):
            op = self._previous()
            right = self._additive()
            expr = BinaryOpNode(location=op.location, left=expr, operator=op.type, right=right)
        return expr

    def _additive(self) -> ExpressionNode:
        expr = self._multiplicative()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = self._previous()
            right = self._multiplicative()
            expr = BinaryOpNode(location=op.location, left=expr, operator=op.type, right=right)
        return expr

    def _multiplicative(self) -> ExpressionNode:
        expr = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self._previous()
            right = self._unary()
            expr = BinaryOpNode(location=op.location, left=expr, operator=op.type, right=right)
        return expr

    def _unary(self) -> ExpressionNode:
        if self._match(TokenType.MINUS, TokenType.NOT):
            op = self._previous()
            operand = self._unary()
            return UnaryOpNode(location=op.location, operator=op.type, operand=operand)
        return self._postfix()

    def _postfix(self) -> ExpressionNode:
        expr = self._primary()

        while True:
            if self._match(TokenType.LPAREN):
                # Function or class call
                lparen_tok = self._previous()
                args: List[CallArg] = []
                self._skip_newlines()
                if not self._check(TokenType.RPAREN):
                    args.append(self._call_arg())
                    self._skip_newlines()
                    while self._match(TokenType.COMMA):
                        self._skip_newlines()
                        if self._check(TokenType.RPAREN):
                            break
                        args.append(self._call_arg())
                        self._skip_newlines()
                self._consume(TokenType.RPAREN, "Expected ')' after argument list.")
                expr = CallNode(location=lparen_tok.location, callee=expr, arguments=args)
            elif self._match(TokenType.LBRACKET):
                # Index access
                lbracket_tok = self._previous()
                self._skip_newlines()
                index_expr = self._expression()
                self._skip_newlines()
                self._consume(TokenType.RBRACKET, "Expected ']' after index expression.")
                expr = IndexNode(location=lbracket_tok.location, target=expr, index=index_expr)
            elif self._match(TokenType.DOT):
                # Member access
                dot_tok = self._previous()
                if self._peek().type == TokenType.IDENTIFIER or self._peek().lexeme in KEYWORDS:
                    name_tok = self._advance()
                else:
                    name_tok = self._consume(TokenType.IDENTIFIER, "Expected property or method name after '.'.")
                expr = MemberAccessNode(location=dot_tok.location, target=expr, member=name_tok.lexeme)
            else:
                break

        return expr

    def _call_arg(self) -> CallArg:
        # Check if it is a named argument: name = expr or name: expr (Dart/Flutter style)
        if self._check(TokenType.IDENTIFIER) and self._peek_next().type in (TokenType.EQUAL, TokenType.COLON):
            name_tok = self._advance()
            self._advance() # Consume '=' or ':'
            val = self._expression()
            return CallArg(name=name_tok.lexeme, value=val)
        val = self._expression()
        return CallArg(name=None, value=val)

    def _primary(self) -> ExpressionNode:
        if self._match(TokenType.INTEGER):
            tok = self._previous()
            return LiteralNode(location=tok.location, value=tok.value, literal_type="Integer")

        if self._match(TokenType.DECIMAL):
            tok = self._previous()
            return LiteralNode(location=tok.location, value=tok.value, literal_type="Decimal")

        if self._match(TokenType.TEXT):
            tok = self._previous()
            return LiteralNode(location=tok.location, value=tok.value, literal_type="Text")

        if self._match(TokenType.TRUE):
            tok = self._previous()
            return LiteralNode(location=tok.location, value=True, literal_type="Boolean")

        if self._match(TokenType.FALSE):
            tok = self._previous()
            return LiteralNode(location=tok.location, value=False, literal_type="Boolean")

        if self._match(TokenType.NULL):
            tok = self._previous()
            return LiteralNode(location=tok.location, value=None, literal_type="Null")

        if self._match(TokenType.SELF):
            tok = self._previous()
            return SelfNode(location=tok.location)

        if self._match(TokenType.IDENTIFIER):
            tok = self._previous()
            return IdentifierNode(location=tok.location, name=tok.lexeme)

        if self._match(TokenType.LPAREN):
            expr = self._expression()
            self._consume(TokenType.RPAREN, "Expected ')' after expression.")
            return expr

        if self._match(TokenType.LBRACKET):
            # List literal
            lbracket_tok = self._previous()
            elements: List[ExpressionNode] = []
            self._skip_newlines()
            if not self._check(TokenType.RBRACKET):
                elements.append(self._expression())
                self._skip_newlines()
                while self._match(TokenType.COMMA):
                    self._skip_newlines()
                    if self._check(TokenType.RBRACKET):
                        break
                    elements.append(self._expression())
                    self._skip_newlines()
            self._consume(TokenType.RBRACKET, "Expected ']' to close list literal.")
            return ListNode(location=lbracket_tok.location, elements=elements)

        if self._match(TokenType.LBRACE):
            # Map literal
            lbrace_tok = self._previous()
            entries: List[Tuple[ExpressionNode, ExpressionNode]] = []
            self._skip_newlines()
            if not self._check(TokenType.RBRACE):
                key = self._expression()
                self._consume(TokenType.COLON, "Expected ':' after key in map entry.")
                val = self._expression()
                entries.append((key, val))
                self._skip_newlines()
                while self._match(TokenType.COMMA):
                    self._skip_newlines()
                    if self._check(TokenType.RBRACE):
                        break
                    key = self._expression()
                    self._consume(TokenType.COLON, "Expected ':' after key in map entry.")
                    val = self._expression()
                    entries.append((key, val))
                    self._skip_newlines()
            self._consume(TokenType.RBRACE, "Expected '}' to close map literal.")
            return MapNode(location=lbrace_tok.location, entries=entries)

        if self._match(TokenType.FUNCTION, TokenType.DEFINE) or (self._check(TokenType.TO) and self._peek_next().type in (TokenType.IDENTIFIER, TokenType.LPAREN)):
            if self._check(TokenType.TO):
                self._advance()
            fn_tok = self._previous()
            fn_name = ""
            if self._check(TokenType.IDENTIFIER):
                fn_name = self._advance().lexeme
            self._consume(TokenType.LPAREN, "Expected '(' after function.")
            params: List[str] = []
            if not self._check(TokenType.RPAREN):
                params.append(self._consume(TokenType.IDENTIFIER, "Expected parameter name.").lexeme)
                while self._match(TokenType.COMMA):
                    params.append(self._consume(TokenType.IDENTIFIER, "Expected parameter name after ','.").lexeme)
            self._consume(TokenType.RPAREN, "Expected ')' after parameter list.")
            self._match(TokenType.COLON)
            self._skip_newlines()
            body = self._block_until(TokenType.END)
            self._consume(TokenType.END, "Expected 'end' to close function.")
            return FunctionDefNode(location=fn_tok.location, name=fn_name, parameters=params, body=body)

        tok = self._peek()
        raise StarSyntaxError(
            f"Unexpected token '{tok.lexeme or tok.type.name}' in expression.",
            tok.location,
            "Check for a missing operand, parenthesis, or valid expression syntax.",
            self.source_code
        )
