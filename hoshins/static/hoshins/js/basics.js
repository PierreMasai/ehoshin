var app = app || {};

app.getUrlResource = function (resourceName) {
    var url = ['', TEAM_NAME, 'api', resourceName];
    return url.join('/');
};

app.Toogler = React.createClass({
    displayName: 'Toogler',

    mixins: [br.formHelper],
    render: function () {
        var dropdown_type = "";
        if (this.props.right) dropdown_type = "dropdown-menu-right";

        var deleteHandler = this.delete;
        if (typeof this.props.deleteHandler !== "undefined") deleteHandler = this.props.deleteHandler;

        var modifyHandler = this.modify;
        if (typeof this.props.modifyHandler !== "undefined") modifyHandler = this.props.modifyHandler;

        return React.createElement(
            'div',
            { className: this.props.classe_names },
            React.createElement(
                'button',
                { type: 'button', className: 'btn flat btn-default dropdown-toggle', 'data-toggle': 'dropdown', 'aria-haspopup': 'true', 'aria-expanded': 'false' },
                React.createElement('span', { className: 'caret' })
            ),
            React.createElement(
                'ul',
                { className: dropdown_type + " dropdown-menu" },
                React.createElement(
                    'li',
                    null,
                    React.createElement(
                        'a',
                        { href: '#', onClick: deleteHandler },
                        'Delete'
                    )
                ),
                React.createElement(
                    'li',
                    null,
                    React.createElement(
                        'a',
                        { href: '#', onClick: modifyHandler },
                        'Modify'
                    )
                )
            )
        );
    }
});

app.aToogler = React.createClass({
    displayName: 'aToogler',

    mixins: [BreakLine.formHelper],
    render: function () {
        var dropdown_type = "";
        if (this.props.right) dropdown_type = "dropdown-menu-right";

        var deleteHandler = this.delete;
        if (typeof this.props.deleteHandler !== "undefined") deleteHandler = this.props.deleteHandler;

        var modifyHandler = this.modify;
        if (typeof this.props.modifyHandler !== "undefined") modifyHandler = this.props.modifyHandler;

        return React.createElement(
            'div',
            { className: this.props.classe_names },
            React.createElement(
                'a',
                { href: '', type: 'button', className: 'dropdown-toggle', 'data-toggle': 'dropdown', 'aria-haspopup': 'true', 'aria-expanded': 'false' },
                React.createElement('span', { className: 'caret' })
            ),
            React.createElement(
                'ul',
                { className: dropdown_type + " dropdown-menu" },
                React.createElement(
                    'li',
                    null,
                    React.createElement(
                        'a',
                        { href: '#', onClick: deleteHandler },
                        'Delete'
                    )
                ),
                React.createElement(
                    'li',
                    null,
                    React.createElement(
                        'a',
                        { href: '#', onClick: modifyHandler },
                        'Modify'
                    )
                )
            )
        );
    }
});

app.Option = React.createClass({
    displayName: 'Option',

    render: function () {
        return React.createElement(
            'option',
            { value: this.props.value },
            this.props.text
        );
    }
});

app.Dropdown = React.createClass({
    displayName: 'Dropdown',

    getInitialState: function () {
        if (_.isUndefined(this.props.default)) this.props.default = "";

        return this.props;
    },
    valueHandleChange: function (event) {
        var value = event.target.value;
        this.setState({ defaultValue: value });

        if (typeof this.state.valueHandleChange === "function") this.state.valueHandleChange(value);
    },
    render: function () {
        var index = 0;
        var options = this.state.options.map(function (option) {
            if (typeof option === "string") return React.createElement(app.Option, { value: option, text: option, key: index++ });else return React.createElement(app.Option, { value: option.value, text: option.text, key: index++ });
        });

        return React.createElement(
            'select',
            { className: 'form-control', value: this.state.defaultValue, onChange: this.valueHandleChange },
            options
        );
    }
});