var app = app || {};

app.getUrlResource = function(resourceName) {
    var url = ['', TEAM_NAME, 'api', resourceName];
    return url.join('/');
};

app.Toogler = React.createClass({
    mixins: [br.formHelper],
    render: function() {
        var dropdown_type = "";
        if(this.props.right)
            dropdown_type = "dropdown-menu-right";

        var deleteHandler = this.delete;
        if(typeof this.props.deleteHandler !== "undefined")
            deleteHandler = this.props.deleteHandler;

        var modifyHandler = this.modify;
        if(typeof this.props.modifyHandler !== "undefined")
            modifyHandler = this.props.modifyHandler;

        return (
            <div className={this.props.classe_names}>
                <button type="button" className="btn flat btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <span className="caret"></span>
                </button>
                <ul className={dropdown_type + " dropdown-menu"}>
                    <li><a href="#" onClick={deleteHandler}>Delete</a></li>
                    <li><a href="#" onClick={modifyHandler}>Modify</a></li>
                </ul>
            </div>
        );
    }
});

app.aToogler = React.createClass({
    mixins: [BreakLine.formHelper],
    render: function() {
        var dropdown_type = "";
        if(this.props.right)
            dropdown_type = "dropdown-menu-right";

        var deleteHandler = this.delete;
        if(typeof this.props.deleteHandler !== "undefined")
            deleteHandler = this.props.deleteHandler;

        var modifyHandler = this.modify;
        if(typeof this.props.modifyHandler !== "undefined")
            modifyHandler = this.props.modifyHandler;

        return (
            <div className={this.props.classe_names}>
                <a href="" type="button" className="dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <span className="caret" />
                </a>
                <ul className={dropdown_type + " dropdown-menu"}>
                    <li><a href="#" onClick={deleteHandler}>Delete</a></li>
                    <li><a href="#" onClick={modifyHandler}>Modify</a></li>
                </ul>
            </div>
        );
    }
});

app.Option = React.createClass({
    render: function() {
        return (
            <option value={this.props.value}>{this.props.text}</option>
        );
    }
});

app.Dropdown = React.createClass({
    getInitialState: function() {
        if(_.isUndefined(this.props.default))
            this.props.default = "";

        return this.props;
    },
    valueHandleChange: function(event) {
        var value = event.target.value;
        this.setState({defaultValue: value});

        if(typeof this.state.valueHandleChange === "function")
            this.state.valueHandleChange(value);
    },
    render: function() {
        var index = 0;
        var options = this.state.options.map(function(option) {
            if(typeof option === "string")
                return <app.Option value={option} text={option} key={index++}/>;
            else
                return <app.Option value={option.value} text={option.text} key={index++}/>;
        });

        return (
            <select className="form-control" value={this.state.defaultValue} onChange={this.valueHandleChange}>
                {options}
            </select>
        );
    }
});