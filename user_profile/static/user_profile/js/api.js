// api url
const api_url = "/api/students/";
  
// Defining async function
async function getapi(url) {
    
    // Storing response
    const response = await fetch(url);
    
    // Storing data in form of JSON
    var data = await response.json();
    console.log(data);
    if (response) {
        hideloader();
    }
    show(data);
}
// Calling that async function
getapi(api_url);
  
// Function to hide the loader
function hideloader() {
    document.getElementById('loading').style.display = 'none';
}
// Function to define innerHTML for HTML table
function show(data) {
	console.log(typeof data)
    let tab = 
        `<tr>
          <th>Id</th>
          <th>User_Profile</th>
          <th>Qualification</th>
          <th>Start_year</th>
         </tr>`;
    
    // Loop to access all rows 
    for (let i = 0; i < data.length; i++) {
    	let r = data[i]
        tab += `<tr> 
    <td>${r.id} </td>
    <td>${r.user_profile}</td>
    <td>${r.qualification}</td> 
    <td>${r.start_year}</td>          
</tr>`;
    }
    // Setting innerHTML as tab variable
    document.getElementById("students").innerHTML = tab;
}


// $(document).on('click', 'button[name="get_student"]', function(){
// 		$.ajax({
// 			url: '/api/students/',
// 			type: "GET",
// 			dataType: "json",
// 			success: function( json ){
// 				console.log(JSON.stringify(json))
// 				new_elements = JSON.stringify(json)
// 				// alert.(new_elements)
// 				$('#students').append( $(`<p> ${new_elements} </p>`) );
// 			}
// 		});
// });