/******* SEARCH AND UPDATE VIEW MODEL *******/
function SearchUpdateViewModel() {
    var self = this;

    self.serverConfig = ko.observable("");
    self.visible = ko.observable(false);

    self.search = function() {
        if (ServerConfigViewModel.serverName() == "") {
            AlertsViewModel.displayError("You must enter a server name!");
        }
        else {
            // get XML configuration, catch callback message (allow editing on success)
            $.get("/api/get_server_XML/" + ServerConfigViewModel.serverName(), function(data) {
                if (data != "Node does not exist.") {
                    self.show();
                    self.serverConfig(vkbeautify.xml(data));
                }
                else {
                    self.hide();
                    AlertsViewModel.displayError("Node " + ServerConfigViewModel.serverName() + " does not exist!");
                }
            });
        }
    };

    self.pushConfig = function() {
        // post JSON dictionary to server, catch callback message
        var data = {"XML" : self.serverConfig(),
                    "serverName" : ServerConfigViewModel.serverName()};
        $.post("/api/update_server_XML/" + ServerConfigViewModel.serverName(), data, function(data) {
            if (data == "Node successfully updated.") {
                AlertsViewModel.displaySuccess("Node " + ServerConfigViewModel.serverName() + " was successfully updated!");
            }
            else {
                AlertsViewModel.displayError(data);
            }
        });
    };

    self.validateXML = function() {
        // parse XML doc and see if it has parsing errors
        var XMLParser = new DOMParser();
        var XMLDoc = XMLParser.parseFromString(self.serverConfig(),"text/xml");

        if (XMLDoc.getElementsByTagName("parsererror").length > 0) {
            var XMLString = new XMLSerializer().serializeToString(XMLDoc.documentElement);
            AlertsViewModel.displayError("Error detected in XML syntax!");
        }
        else { // push the configuration if no errors were found
            self.pushConfig();
        }
    };

    self.deleteConfig = function() {
        if (confirm("Please confirm that you want to delete the configuration for " + ServerConfigViewModel.serverName() + " by pressing OK.")) {
            // attempt to delete the server configuration, catch callback message
            $.get("/api/delete_server/" + ServerConfigViewModel.serverName(), function(data) {
                if (data == 'Node successfully deleted.') {
                    AlertsViewModel.displaySuccess("Node " + ServerConfigViewModel.serverName() + " was successfully deleted!");
                    ServerConfigViewModel.getAllServerNames();
                    self.hide();
                }
                else {
                    AlertsViewModel.displayError(data);
                }
            });
        }
    };

    self.editedConfig = function() {
        var serverConfigDiv = document.getElementsByName("server-config")[0];
        var newConfig = serverConfigDiv.textContent;

        self.serverConfig(newConfig);
    };

    self.closeAlerts = function() {
        AlertsViewModel.closeAlerts();
    };


    self.hide = function() {
        self.visible(false);
    };

    self.show = function() {
        self.visible(true);
    };

    self.tearDown = function() {
        self.serverConfig("");
        self.hide();
    }
}