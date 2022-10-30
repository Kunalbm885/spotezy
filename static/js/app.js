let navigation = document.querySelector(".navigation");
let toggle = document.querySelector(".toggle");
let main_right = document.querySelector(".main_right");
toggle.onclick = function () {
  navigation.classList.toggle("active");
  main_right.classList.toggle("active");
};

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $(".image-upload-wrap").hide();

      $(".file-upload-image").attr("src", e.target.result);
      $(".file-upload-content").show();

      $(".image-title").html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);
  } else {
    removeUpload();
  }
}

function removeUpload() {
  $(".file-upload-input").replaceWith($(".file-upload-input").clone());
  $(".file-upload-content").hide();
  $(".image-upload-wrap").show();
}
 $(".image-upload-wrap").bind("dragover", function () {
  $(".image-upload-wrap").addClass("image-dropping");
});
  $(".image-upload-wrap").bind("dragleave", function () {
  $(".image-upload-wrap").removeClass("image-dropping");
});


function initialize() {
  var mapOptions,
    map,
    marker,
    searchBox,
    city,
    infoWindow = "",
    addressEl = document.querySelector("#map-search"),
    latEl = document.querySelector(".latitude"),
    longEl = document.querySelector(".longitude"),
    element = document.getElementById("map-canvas");
  city = document.querySelector(".reg-input-city");

  mapOptions = {
    zoom: 100,
    // Current Lat and Long position of the pin/
    center: new google.maps.LatLng(18.9220, 72.8347),

    disableDefaultUI: false, // Disables the controls like zoom control on the map if set to true
    scrollWheel: true, // If set to false disables the scrolling on the map.
    draggable: true, // If set to false , you cannot move the map around.
    // mapTypeId: google.maps.MapTypeId.HYBRID, // If set to HYBRID its between sat and ROADMAP, Can be set to SATELLITE as well.
    // maxZoom: 11, // Wont allow you to zoom more than this
    // minZoom: 9  // Wont allow you to go more up.
  };

  /**
   * Creates the map using google function google.maps.Map() by passing the id of canvas and
   * mapOptions object that we just created above as its parameters.
   *
   */
  // Create an object map with the constructor function Map()
  map = new google.maps.Map(element, mapOptions); // Till this like of code it loads up the map.

  /**
   * Creates the marker on the map
   *
   */
  marker = new google.maps.Marker({
    position: mapOptions.center,
    map: map,
    // icon: 'http://pngimages.net/sites/default/files/google-maps-png-image-70164.png',
    draggable: true,
  });

  /**
   * Creates a search box
   */
  var searchBox = new google.maps.places.SearchBox(addressEl);
  // var place = autocomplete.getPlace(searchBox);
  // var inputValue = searchBox.name + " " + searchBox.formatted_address;
  // console.log(inputValue");
  /**
   * When the place is changed on search box, it takes the marker to the searched location.
   */
  google.maps.event.addListener(searchBox, "places_changed", function () {
    var places = searchBox.getPlaces(),

      bounds = new google.maps.LatLngBounds(),
      i,
      place,
      lat,
      long,
      resultArray,
      addresss = places[0].name + " " + places[0].formatted_address;

    for (i = 0; (place = places[i]); i++) {
      bounds.extend(place.geometry.location);
      marker.setPosition(place.geometry.location); // Set marker position new.
    }

    map.fitBounds(bounds); // Fit to the bound
    map.setZoom(100); // This function sets the zoom to 15, meaning zooms to level 15.

    lat = marker.getPosition().lat();
    long = marker.getPosition().lng();
    latEl.value = lat;
    longEl.value = long;

    resultArray = places[0].address_components;

    // Get the city and set the city input value to the one selected
    for (var i = 0; i < resultArray.length; i++) {
      if (
        resultArray[i].types[0] &&
        "administrative_area_level_2" === resultArray[i].types[0]
      ) {
        citi = resultArray[i].long_name;
        city.value = citi;
      }
    }

    // Closes the previous info window if it already exists
    if (infoWindow) {
      infoWindow.close();
    }
    /**
     * Creates the info Window at the top of the marker
     */
    infoWindow = new google.maps.InfoWindow({
      content: addresss,
      
    });


    infoWindow.open(map, marker);

    // var test = document.getElementById("dest").value = infoWindow.content;

    var test2 = document.getElementById("map-search").innerText = infoWindow.content;
    // console.log(test)
    console.log("from main " + test2)

    console.log(infoWindow.content)

  });

  /**
   * Finds the new position of the marker when the marker is dragged.
   */
  google.maps.event.addListener(marker, "dragend", function (event) {
    var lat, long, address, resultArray, citi;

    console.log("i am dragged");
    lat = marker.getPosition().lat();
    long = marker.getPosition().lng();

    var geocoder = new google.maps.Geocoder();
    geocoder.geocode(
      { latLng: marker.getPosition() },
      function (result, status) {
        if ("OK" === status) {
          // This line can also be written like if ( status == google.maps.GeocoderStatus.OK ) {
          address = result[0].formatted_address;
          resultArray = result[0].address_components;

          // Get the city and set the city input value to the one selected
          for (var i = 0; i < resultArray.length; i++) {
            if (
              resultArray[i].types[0] &&
              "administrative_area_level_2" === resultArray[i].types[0]
            ) {
              citi = resultArray[i].long_name;
              console.log(citi);
              city.value = citi;
            }
          }
          addressEl.value = address;
          latEl.value = lat;
          longEl.value = long;
        } else {
          console.log(
            "Geocode was not successful for the following reason: " + status
          );
        }

        // Closes the previous info window if it already exists
        if (infoWindow) {
          infoWindow.close();
        }

        /**
         * Creates the info Window at the top of the marker
         */
        infoWindow = new google.maps.InfoWindow({
          content: address,
        });

        infoWindow.open(map, marker);
      }
    );
  });
}
