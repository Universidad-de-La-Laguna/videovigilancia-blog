var pluscomments = pluscomments || {};

pluscomments.load = function(apiKey) {
  gapi.client.load('plus', 'v1', pluscomments.go);
  gapi.client.setApiKey(apiKey);
}

// search for g-comments-for classes
pluscomments.go = function() {
  //  Find the comment elements to process
  var fetchElements = document.getElementsByClassName('g-comments-for');
  for (var i=0; i < fetchElements.length; i++) {
    var activityId = fetchElements[i].classList[1];
    pluscomments.fetchComments(activityId);
  }
}

pluscomments.fetchComments = function(activityId) {
  var rpcBatch = gapi.client.newRpcBatch();
  var activitiesGet = gapi.client.plus.activities.get({
    'activityId': activityId,
  });
  var commentsList = gapi.client.plus.comments.list({
    'activityId': activityId,
    'maxResults': '100'
  });
  rpcBatch.add(activitiesGet, {
    'id': 'activity'
  });
  rpcBatch.add(commentsList, {
    'id': 'comments'
  });
  rpcBatch.execute(pluscomments.parseComments);
}

pluscomments.parseComments = function(responseJson) {
  var activity = responseJson['activity'].result;
  var comments = responseJson['comments'].result.items;

  //find element to insert into
  var insertionElements =
      document.getElementsByClassName('g-comments-for ' + activity.id);
  var insertionElement = insertionElements[0];

  var innerHTML = "";
  if (typeof(comments) != "undefined") {
    var newContents = "";
    for (i = 0; i < comments.length; i++) {
      var actor = comments[i].actor;

      var commentBody = comments[i].object.content;

      //do the insertion
      newContents += "<dt><a href='" + actor.url + "'><img src='" +
          actor.image.url + "'></a></dt>" + "<dd><a href='" + actor.url + "'>" +
          actor.displayName + "</a>: " + commentBody + "</dd>";
    }
    innerHTML = "<dl>" + newContents + "</dl> ";
  }
  insertionElement.innerHTML = innerHTML +
      "<p class='g-commentlink'>Por favor, comenta a través del <a href='" +
      activity.url + "'>artículo en Google+</a>.</p>";
}
