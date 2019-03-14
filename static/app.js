/* Xiulong Liu
 * EE 568 Final Project
 */
(function() {

    // Global JSON object to contain quotes. This is a global to prevent
    // long waiting times.
    let json;

    window.addEventListener("load", initialize);

    /**
     * When the page loads, call the API to populate the page with the first quote.
     */
    function initialize() {
      initialView();
      $("upload-btn").addEventListener("click", postImage);
      $("process").addEventListener("click", requestProcessedImage);
    }

    function initialView() {
      let input = document.querySelector('input');
      let preview = document.querySelector('.preview');
      input.style.opacity = 0;
      input.addEventListener('change', updateImageDisplay);
    }

     function postImage() {
       let imageFile = $("image-upload").files[0];
       let formdata = new FormData();
       formdata.append("file", imageFile);
       jQuery.ajax({
            // Your server script to process the upload
            url: '/image',
            type: 'POST',
            // Form data
            data: formdata,
            // Tell jQuery not to process data or worry about content-type
            cache: false,
            contentType: false,
            processData: false,
            success: function (msg) {
               let success = msg["success"];
               $("msg").innerText = success;
               setTimeout(()=>{$("msg").innerText = "";}, 3000);
            },
            error: function (jqXHR, textStatus, errorThrown) {
               $("msg").innerText = textStatus + ": " + errorThrown;
            }
        });
    }

    function updateImageDisplay() {
      let input = document.querySelector('input');
      let preview = document.querySelector('.preview');
      while(preview.firstChild) {
            preview.removeChild(preview.firstChild);
      }
      let curFile = input.files;
       if(curFile.length == 0) {
          let para = document.createElement('p');
          para.textContent = 'No files currently selected for upload';
          preview.appendChild(para);
       }
       else {
          //let list = document.createElement('li');
          if (isFileValid(curFile[0])) {
              let image = document.createElement('img');
              image.src = window.URL.createObjectURL(curFile[0]);
              image.style.width = "300px";
              image.style.display = "block";
              image.style.margin = "auto auto";
              image.style.marginTop = "30px";
              preview.appendChild(image);
          }
        }
    }

   function isFileValid(file) {
     let fileTypes = ['image/jpeg','image/pjpeg','image/png'];
     for(var i = 0; i < fileTypes.length; i++) {
       if(file.type == fileTypes[i]) {
          return true;
       }
      }
      return false;
   }

    /**
     * Choose a random quote and author and append them to the page.
     */
    function updatePage() {
        let quote = $("quote");
        let author = $("author");
        let choice = json[Math.floor(Math.random() * json.length)];
        quote.innerHTML = "Quote: " + choice["Quote"];
        author.innerHTML = "Author: " + choice["Author"];
    }

    function requestProcessedImage() {
      let approach = $("approach").value;
      let cluster = $("cluster").value;
      let url = "/result?" + "approach=" + approach;
      console.log(url)
      if (approach === "GMM" || approach === "kmeans") {
        url += "&" + "cluster=" + cluster;
      }
      displayResult(url);
    }

    function displayResult(url) {
      $("out-img").innerHTML = "";
      let xhr = new XMLHttpRequest();
      xhr.open('GET', url, true);
      xhr.responseType = "blob";
      xhr.onload = function() {
        let blob = this.response;
        let img = document.createElement("img");
        img.id = "image";
        img.src = window.URL.createObjectURL(blob);
        img.style.width = "300px";
        img.display = "block";
        img.style.margin = "auto auto";
        img.style.marginTop = "30px";
        $("out-img").appendChild(img);
      };
      xhr.send();
    }

    // Shorthand function for document.getElementById
    function $(id) {
        return document.getElementById(id);
    }

     /** Helper function to return the response's result text if successful, otherwise
      * returns the rejected Promise result with an error status and corresponding text
      * @param {object} response - response to check for success/error
      * @return {object} - valid result text if response was successful, otherwise rejected
      *                    Promise result
      */
    function checkStatus(response) {
        if (response.status >= 200 && response.status < 300 || response.status == 0) {
            return response.text();
        } else {
            return Promise.reject(new Error(response.status + ": " + response.statusText));
        }
    }
})();
