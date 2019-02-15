'use strict';

(function () {


  const api_url = 'https://eu-west-1a.online.tableau.com/api/3.2'
  const auth_url = 'https://eu-west-1a.online.tableau.com/api/3.2/auth/signin'
  const username = ''
  const password = ''
  const site = ''

$(document).ready(function () {

  const tabserver_connect = async function(username
    , password, site, view_name) {

    var auth_url = `${api_url}/auth/signin`

    var credentials = {
      "credentials": {
          "name": username,
          "password": password,
          "site": {
              "contentUrl": site
          }
      }
    }

    var auth_response =  await sendHttp({
      method : 'POST',
      endpoint: auth_url,
      body: JSON.stringify(credentials)
    })

  var token = auth_response.credentials.token
  var site_id = auth_response.credentials.site.id

  var search_view_url = `${api_url}/sites/${site_id}/views`

  var views = await sendHttp({
    method: 'GET',
    endpoint: search_view_url,
    body: " ",
    X_tableau_auth : token
  })

  var views_list = views["views"]['view']
  var keyword_search = view_name
  var view_id = views_list.filter(function(arr){return arr.name == view_name})[0].id

  var pdf_url = `${api_url}/sites/${site_id}/views/${view_id}/pdf`
  var pdf_ = await sendHttp({
    method: 'GET',
    endpoint: pdf_url,
    body: " ",
    X_tableau_auth : token,
    pdf: true
  })


}


  var sendHttp = function (params) {
    return new Promise((resolve) => {
      var xhr = new XMLHttpRequest();
      xhr.open(params.method, params.endpoint, true);

      if("X_tableau_auth" in params) {
        console.log(params.X_tableau_auth)
        xhr.setRequestHeader("X-tableau-auth",params.X_tableau_auth);
      }

      if("pdf" in params) {
        var pdf = params.endpoint
        xhr.onload = function() {
          var d = this.responseText
          let a = document.createElement("a");
          a.href = "data:application/octet-stream;base64,"+encodeURI(d);
          document.body.appendChild(a)
          window.open(a.href)
          a.download = "documentName.pdf"
          a.click();
          a.remove()
      }
    }
    else {
      xhr.setRequestHeader("Content-type", "application/json");
      xhr.setRequestHeader("Accept", 'application/json');
      xhr.onload = function () {
        resolve(JSON.parse(this.responseText));
      };
    }
      xhr.send(
        params.body
      );

    })
  }
  var token = tabserver_connect(username, password, site, "Cost of a night out")

    // Tell Tableau we'd like to initialize our extension
    tableau.extensions.initializeAsync().then(function () {

      // Get the dashboard name from the tableau namespace and set it as our title
      const dashboardName = tableau.extensions.dashboardContent.dashboard.name;
      $('#choose_sheet_title').text(dashboardName);
    });
  });
})();
