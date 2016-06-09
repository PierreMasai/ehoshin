var app = app || {};

function changeHoshin(model) {
    url = ['', TEAM_NAME, model.attributes.id];
    app.router.navigate(url.join('/'), { trigger: true });
}

app.HoshinItemView = React.createClass({
    displayName: 'HoshinItemView',

    mixins: [br.formHelper],
    changeHoshin: function (event) {
        event.preventDefault();
        changeHoshin(this.props.model);
    },
    del: function (event) {
        var deleted = function () {
            app.router.navigate('/' + TEAM_NAME, { trigger: true });
        };

        this.delete(event, deleted);
    },
    render: function () {
        var data = this.props.model.attributes;
        var managePart = "";
        var size = "col-sm-12";
        if (USER.isModerator) {
            managePart = React.createElement(app.Toogler, { model: this.props.model, classe_names: 'col-sm-1',
                right: true, deleteHandler: this.del });
            size = "col-sm-11";
        }

        return React.createElement(
            'div',
            { className: 'row' },
            React.createElement(
                'div',
                { className: 'col-sm-12 hoshin_menu_box' },
                React.createElement(
                    'a',
                    { className: size + " show", href: '#', onClick: this.changeHoshin },
                    React.createElement(
                        'button',
                        { className: 'btn flat btn-default hoshins_items', 'aria-label': 'Left Align' },
                        React.createElement(
                            'span',
                            { style: { backgroundColor: data.color } },
                            ' '
                        ),
                        React.createElement(
                            'span',
                            null,
                            data.name
                        )
                    )
                ),
                managePart
            )
        );
    }
});

app.HoshinFormView = React.createClass({
    displayName: 'HoshinFormView',

    mixins: [BreakLine.formHelper],
    fields: {
        "name": "Name"
    },
    verify: function () {
        var errors = {};
        var data = this.state.model.attributes;

        if (_.isUndefined(data.name) || data.name === "") errors['name'] = ['This field must not be blank'];

        return errors;
    },
    bgHandleChange: function (event) {
        this.setAttribute("color", event.color.toHex());
    },
    componentDidMount: function () {
        var DOMNode = ReactDOM.findDOMNode(this);
        $(DOMNode).find(".color").colorpicker({ format: "hex" }).on('changeColor.colorpicker', this.bgHandleChange);
    },
    save: function (event) {
        this.saveModel(event, changeHoshin);
    },
    render: function () {
        var data = this.state.model.attributes;
        var style = {
            backgroundColor: data.color
        };

        var className = "row";
        if (this.props.model._isOptimistic) className += " isOptimistic";

        return React.createElement(
            'div',
            { className: className },
            React.createElement(
                'div',
                { className: 'col-sm-12' },
                React.createElement(
                    'span',
                    { type: 'button', className: 'btn flat btn-default', 'aria-label': 'Left Align' },
                    React.createElement(BreakLine.Errors, { errors: this.state.model._errors }),
                    React.createElement(
                        'div',
                        { className: 'input-group' },
                        React.createElement(
                            'span',
                            { className: 'input-group-addon color' },
                            React.createElement(
                                'i',
                                { className: 'add-on', style: style },
                                '    '
                            )
                        ),
                        React.createElement('input', { type: 'text', className: 'form-control ', 'data-model': 'name', placeholder: 'Name', value: data.name, onChange: this.valueHandleChange }),
                        React.createElement(
                            'a',
                            { className: 'input-group-addon', href: '#', onClick: this.save },
                            'Save'
                        )
                    )
                )
            )
        );
    }
});

app.HoshinList = br.List.extend({
    ItemView: app.HoshinItemView,
    FormView: app.HoshinFormView,
    url: app.getUrlResource('hoshins'),
    defaults: {
        color: "#81b9c3",
        owner: USER
    },
    render: function (Nodes, modelForm) {
        var formPart = "";

        if (USER.isModerator) formPart = React.createElement(this.FormView, { model: modelForm });

        return React.createElement(
            'div',
            null,
            Nodes,
            formPart
        );
    }
});

app.HoshinIndicator = React.createClass({
    displayName: 'HoshinIndicator',

    render: function () {
        var style = {
            backgroundColor: this.props.color
        };
        return React.createElement(
            'div',
            { className: 'indicator panel panel-default' },
            React.createElement(
                'div',
                { className: 'panel-heading indicator_part without_border', style: style },
                React.createElement('img', { src: ICONS_URL + this.props.picture_name, height: '30' })
            ),
            React.createElement(
                'div',
                { className: 'panel-body indicator_part' },
                React.createElement(
                    'div',
                    { className: 'span6 center' },
                    React.createElement(
                        'span',
                        null,
                        this.props.value
                    )
                )
            )
        );
    }
});

app.HoshinIndicatorList = React.createClass({
    displayName: 'HoshinIndicatorList',

    render: function () {
        return React.createElement(
            'table',
            { className: 'table' },
            React.createElement(
                'tbody',
                null,
                React.createElement(
                    'tr',
                    null,
                    React.createElement(
                        'td',
                        null,
                        'Themes'
                    ),
                    React.createElement(
                        'td',
                        null,
                        this.props.nb_items
                    )
                ),
                React.createElement(
                    'tr',
                    null,
                    React.createElement(
                        'td',
                        null,
                        'Concrete actions'
                    ),
                    React.createElement(
                        'td',
                        null,
                        this.props.nb_implementation_priorities
                    )
                ),
                React.createElement(
                    'tr',
                    null,
                    React.createElement(
                        'td',
                        null,
                        'Comments'
                    ),
                    React.createElement(
                        'td',
                        null,
                        this.props.nb_comments
                    )
                ),
                React.createElement(
                    'tr',
                    null,
                    React.createElement(
                        'td',
                        null,
                        'Users'
                    ),
                    React.createElement(
                        'td',
                        null,
                        this.props.nb_users
                    )
                ),
                React.createElement(
                    'tr',
                    null,
                    React.createElement(
                        'td',
                        null,
                        'Users who commented once'
                    ),
                    React.createElement(
                        'td',
                        null,
                        this.props.nb_commentators
                    )
                ),
                React.createElement(
                    'tr',
                    null,
                    React.createElement(
                        'td',
                        null,
                        'Users who commented more than once'
                    ),
                    React.createElement(
                        'td',
                        null,
                        this.props.nb_chatty_commentators
                    )
                )
            )
        );
    }
});