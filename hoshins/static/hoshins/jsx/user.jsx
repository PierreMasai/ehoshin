var app = app || {};

{
    var COUNT = undefined;
    app.UserList = br.List.extend({
        url: "/users"
    });

    app.HelpList = br.List.extend({
        url: app.getUrlResource('helps')
    });

    app.Notifications = Backbone.Model.extend({
        url: app.getUrlResource("notifications/api/list/")
    });

    // TODO: handle timestamp formatting
    app.NotificationView = React.createClass({
        markAsRead: function() {
            var id = this.state.id;
            var parent = this;
            $.get(app.getUrlResource("notifications/mark-as-read/"+id))
                .done(function() {
                    parent.setState({unread: false});
                    COUNT -= 1;
                    $("#NbNotifications").html(COUNT);
                })
        },
        redirectTarget: function(event) {
            event.preventDefault();

            if(this.state.unread)
                this.markAsRead();

            app.router.navigate(this.state.data.url, {trigger:true});
            $("#wrapper").toggleClass("toggled");
        },
        getInitialState: function() {
            this.props.model.data = JSON.parse(this.props.model.data);
            return this.props.model;
        },
        render: function() {
            var data = this.state;

            var className = "";
            if(data.unread)
                className = "unread";

            return (
                <li>
                    <a href="" className={className} dangerouslySetInnerHTML={{__html: data.verb}} onClick={this.redirectTarget}>
                    </a>
                </li>
            );
          }
    });

    app.NotificationsView = React.createClass({
        render: function() {
            var notifications = this.props.notifications.map(function(notification) {
                return (<app.NotificationView model={notification} key={notification.id}/>);
            });

            return (
                <ul>
                    {notifications}
                </ul>
            );
          }
    });

    app._NotificationView = Backbone.View.extend({
        initialize: function(data) {
            this.model = data;
            _.bindAll(this, 'render');
            this.model.bind('change', this.render);
            this.model.bind('add',    this.render);
            this.model.bind('remove', this.render);
        },
        render: function(model) {
            if(typeof COUNT === "undefined")
                COUNT = model.attributes.unread_count;
            $("#NbNotifications").html(COUNT);

             ReactDOM.render(
                 React.createElement(app.NotificationsView, { notifications: this.model.attributes.unread_list }),
                                     document.getElementById("notifications")
             );
        }
    });

    app.notifications = new app.Notifications();
    app.notificationsView = new app._NotificationView(app.notifications);
}
