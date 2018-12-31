var myArray = [];
$.getJSON('/safezone', function(jd) {
  $.each(jd.safeZone, function(i, obj) {
    jd.safeZone[i][0][0]+=siderealtime;
    jd.safeZone[i][1][0]+=siderealtime;
    /*if (jd.safeZone[i][0] < 0) {
      jd.safeZone[i][0] = 365 - jd.safeZone[i][0];
    }*/
    myArray.push(jd.safeZone[i]);
  });
});

// Get siderealtime
if (!String.format) {
  String.format = function(format) {
    var args = Array.prototype.slice.call(arguments, 1);
    return format.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}
// Set defaults
var date = "12/26/2018";
var coords="48.4284N, 123.3656W";
var reps="1";
var intmag="1";
var intunit="minutes";
var time="05:00:00.000 AM -7";

// Get siderealtime
var url = String.format("http://api.usno.navy.mil/sidtime?ID=NC&date={0}&coords={1}&reps={2}&intv_mag={3}&intv_unit={4}&time={5}", date, coords, reps, intmag, intunit, time);
var encoded = encodeURI(url);

// from python: siderealtime = json_response['properties']['data'][0]['lmst']
var siderealtime = -1;
$.getJSON(encoded, function(jd) {
  siderealtime = jd.properties.data[0].lmst;
});

var aladin = A.aladin('#aladin-lite-div', {target: siderealtime+" +55", fov: 150});
aladin.addCatalog(A.catalogFromVizieR('VII/118', 'M 31', 50, {onClick: 'showTable'}));

var overlay = A.graphicOverlay({color: '#ee2345', lineWidth: 3});
aladin.addOverlay(overlay);
overlay.addFootprints([A.polygon(myArray)]);
//overlay.add(A.polyline(myArray));

/*var cat = A.catalog({name: 'Some markers', sourceSize: 18});
//A.addCatalog(cat);
for(var i=0;i++;i<myArray.length){
  cat.addSources([A.marker(myArray[i][0],myArray[i][1])]);
}*/

//overlay.add(A.circle(Number(siderealtime), 55.0, 45, {color: 'cyan'})); // radius in degrees
