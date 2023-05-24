function getEmailsByLabel() {
  var label = GmailApp.getUserLabelByName("incidents");
  var threads = label.getThreads(0, 500);
  var sheet = SpreadsheetApp.getActiveSheet();
  var cleanThreads = removeTinkSender(threads);
  Logger.log(cleanThreads.length);
  var columnA;
  var columnB;
  var columnC;
  var columnD;

  //parse threads
  for (var i = 0; i < cleanThreads.length; i++) {

    //get first message in each thread
    var firstMessage = cleanThreads[i].getMessages()[0];

    // remove tink.com senders
    if (!firstMessage.getReplyTo().toString().endsWith("tink.com>")) {
      columnA = "A" + (i + 2);
      columnB = "B" + (i + 2);
      columnC = "C" + (i + 2);
      columnD = "D" + (i + 2);

      cellA = sheet.getRange(columnA);
      cellA.setValue(firstMessage.getPlainBody().trim());
      cellB = sheet.getRange(columnB);
      cellB.setValue(firstMessage.getDate());
      cellC = sheet.getRange(columnC);
      cellC.setValue(firstMessage.getFrom());
      cellD = sheet.getRange(columnD);
      cellD.setValue(firstMessage.getReplyTo());
    }
  }
  return;
}



function removeTinkSender(threads) {
  var cleanThreads = [];

  for (var i = 0; i < threads.length; i++) {
    var firstMessage = threads[i].getMessages()[0];
    if (!firstMessage.getReplyTo().toString().endsWith("tink.com>")) {
      cleanThreads.push(threads[i]);
    }
  }

  return cleanThreads;
}
