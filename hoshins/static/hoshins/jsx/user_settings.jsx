var app = app || {};

MembershipItemView = React.createClass({
    mixins: [BreakLine.formHelper],
    componentDidMount: function() {
        var DOMNode = ReactDOM.findDOMNode(this);
        var parent = this;
        var mode = 'enable';
        if(this.state.model.attributes.member.id == USER.id)
            mode = 'disable';

        $(DOMNode).find('input[type=checkbox][data-toggle^=toggle]')
                .bootstrapToggle(mode)
                .change(function(ev) {
                    var target = $(ev.target);
                    var is_moderator = target.prop('checked') ? 'MO' : 'NO';
                    parent.setAttribute('type', is_moderator);
                    parent.saveModel();
                });

        $(DOMNode).find('.remove-user').click(function( event ) {
            event.preventDefault();
            parent.props.model.destroy();
        });
    },
    render: function() {
        var data = this.state.model.attributes;
        var full_name = data.member.first_name + ' ' + data.member.last_name;

        var checked = (data.type === 'MO' || data.type === 'OW') ? 'checked' : '';

        return (
            <tr>
                <td>{ full_name }</td>
                <td>
                    <input defaultChecked={ checked } type="checkbox" data-toggle="toggle" />
                </td>
                <td><a href=""><span className="glyphicon glyphicon-remove remove-user"/></a></td>
            </tr>
        );
    }
});


MembershipList = br.List.extend({
    ItemView: MembershipItemView,
    url: app.getUrlResource('memberships'),
    render: function (Nodes) {
        return (
            <tbody>
                <tr>
                    <th>User</th>
                    <th>Is moderator</th>
                    <th>Remove</th>
                </tr>
                { Nodes }
            </tbody>
        );
    }
});

membership = new MembershipList('userList');
membership.fetch();

UserList = br.List.extend({
    url: '/users'
});
userList = new UserList('userList');
userList.fetch();


$("#user-filter select").on("change", function() {
    var type = $(this).val();

    if(type == 'All')
        $("#userList tr:nth-child(n+2)").show();
    else {
        $("#userList tr:nth-child(n+2)").each(function() {
            var row = $(this);
            var elt = $(row.find('input[type=checkbox][data-toggle^=toggle]'));

            if(elt.prop('checked').toString() === type)
                row.show();
            else
                row.hide();
        });
    }
});

$("#user-filter input").on("change paste keyup", function() {
    var name = $(this).val().toLowerCase();
    var type = $("#user-filter select").val();

    $("#userList tr:nth-child(n+2)").each(function() {
        var row = $(this);
        var elt_type = $(row.find('input[type=checkbox][data-toggle^=toggle]')).prop('checked').toString();
        var elt_name = $(row.children()[0]).text().toLowerCase();
        if(elt_name.indexOf(name) != -1) {
            if(type == 'All' || type == elt_type)
                row.show();
        }
        else
            row.hide();
    });
});

var substringMatcher = function(elts) {
  return function findMatches(q, cb) {
    var matches, substringRegex;

    // an array that will be populated with substring matches
    matches = [];

    // regex used to determine if a string contains the substring `q`
    substrRegex = new RegExp(q, 'i');

    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
    $.each(elts, function(i, elt) {
      if (substrRegex.test(elt.full_name) || substrRegex.test(elt.username)) {
        matches.push(elt);
      }
    });

    cb(matches);
  };
};

userList.doneFetching(function() {
        var names = _.map(userList.model.models, function(model){
            var d = model.attributes;
            return {full_name: d.first_name + " " + d.last_name, username: d.username};
        });

        $(".typeahead").typeahead(
            {
              hint: true,
              highlight: true,
              minLength: 1
            },
            {
              name: 'names',
              source: substringMatcher(names),
              display: 'username',
              templates: {
                empty: [
                  '<div class="empty-message">',
                    'Unable to find any users that match the current query',
                  '</div>'
                ].join('\n'),
                suggestion: Handlebars.compile('<div>{{full_name}} - <span class="discreet">{{username}}</span></div>'),
              }
            }
        );
    }
);

$("#add-user button").click(function() {
    var input = $("#add-user>form>div>span.twitter-typeahead>input.form-control.typeahead.tt-input");
    var username = input.val();
    input.val("");

    var it = membership.newItem({member: {username: username}, type: 'NO'});
    it.save(null, {
        success: function(){
            $("#error-user").hide();
            membership.model.add(it);
        },
        error: function(){ $("#error-user").show(); }
    });

});