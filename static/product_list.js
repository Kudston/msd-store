// Get the input field and list
const filterInput = document.getElementById('filterInput');
const list = document.getElementById('list');
const items = list.getElementsByTagName('tr');
const order_button = document.getElementById('createOrder')
document.addEventListener('DOMContentLoaded', function() {
  NumberTable();
});
// Add event listener for input changes
filterInput.addEventListener('input', filterList);
order_button.addEventListener('click', CreateOrder)
function filterList() {
  const filterValue = filterInput.value.toLowerCase(); // Convert the input to lowercase for case-insensitive filtering
   
  // Loop through all the list items/
  if(items.length>0)
    {
      for (let i = 0; i < items.length; i++) {
        const item = items[i];
        const tags = item.getElementsByTagName('td')
        let found = false;
        for(let j=0; j<3; j++)
          {
            const tag = tags[j];
            const text = tag.textContent.toLowerCase();
            if (text.indexOf(filterValue) > -1) {
              item.style.display = '';
              found = true;
              break;
            } 
          }
        if (found==true) {
            item.style.display = '';
          } else {
            item.style.display = 'none';
          }
      }
    }
  NumberTable();
      } 
      
function NumberTable() {
  // Loop through all the list items/
  if(items.length>0)
    {
      let counts = 0;
      for (let i = 0; i < items.length; i++) {
        const item = items[i];
        const tags = item.getElementsByTagName('th')
        const tag = tags[0];
        if(item.style.display=="")
        { 
          counts++;
          tag.textContent = counts;
        }
      }
    }
  }
  
var current_order_id = 0;
function CreateOrder() {
    const ordertable = document.getElementById("OrderDiv")
    const get_orderbook = ordertable.getElementsByTagName("thead")
    if(get_orderbook.length>0)
        return;
    fetch('http://localhost:8000/create-order')
    .then((response) => {
        return response.json()})
    .then(data => {
        // Process the received data
        current_order_id = data['id']
        var tbody_element = document.createElement("tbody");
        tbody_element.setAttribute("id", "orderList");
        var theader_element = document.createElement("thead")
        var col0 = document.createElement("th")
        col0.textContent = "#";
        var col1 = document.createElement("th")
        col1.textContent = "name";
        var col2 = document.createElement("th")
        col2.textContent = "quantity";
        var col3 = document.createElement("th")
        col3.textContent = "cost";
        var col4 = document.createElement("th")
        col4.textContent = "Actions";
        theader_element.appendChild(col0)
        theader_element.appendChild(col1)
        theader_element.appendChild(col2)
        theader_element.appendChild(col3)
        theader_element.appendChild(col4)
        ordertable.appendChild(theader_element)
        ordertable.appendChild(tbody_element)
    })
    .catch(error => {
    alert(error);
    });
}

var table = document.querySelector('table');
var order_storage_list = []
// Add event listener to the table
table.addEventListener('click', function(event) {
    // Check if the clicked element is a button
    if (event.target.classList.contains('row-button')) {
    var clickedButton = event.target;
    var clickedRow = clickedButton.closest('tr');
    var tablebody = document.getElementById("orderList");
    if(tablebody===null)
        {
        alert("you need to create an order");
        return;
        }
    
    // Retrieve the contents of the row
    var rowList = []
    var clicked_row_td = clickedRow.getElementsByTagName("td");
    var clicked_row_product_name = clicked_row_td[0].textContent;
    var clicked_row_product_cost = clicked_row_td[1].textContent;
    var form_inputs = clicked_row_td[3].getElementsByTagName('input');
    var form_id_input_value = form_inputs[1].value;
    var form_number_input_value = form_inputs[2].value;
    if(parseInt(form_number_input_value)==0){
        alert('Quantity must be greater than 1');
        return;
    }
    
    var Foundind = findNameInList(order_storage_list, clicked_row_product_name);

    if(Foundind>=0)
    {
        var quantity_left = clicked_row_td[2].textContent;
        var prev_quant = parseInt(order_storage_list[Foundind][3])
        var combinedQuant = prev_quant+parseInt(form_number_input_value);
        if(combinedQuant>parseInt(quantity_left)){
        alert(`current quantity due to existing order is ${quantity_left-prev_quant}`);
        return;
        }
        order_storage_list[Foundind][3] = combinedQuant;
        /////////////
        editOrderList();
        return;
    }
    rowList.push(clicked_row_product_name)
    rowList.push(clicked_row_product_cost)
    rowList.push(form_id_input_value)
    rowList.push(form_number_input_value)
    order_storage_list.push(rowList)
    //////////////////
    editOrderList();
    }
    });

function editOrderList() {
    var tablebody = document.getElementById("orderList")
    var new_tablebody = document.createElement("tbody")
    for(let i=0; i<order_storage_list.length; i++){
        var rowname = order_storage_list[i][0]
        var rowquant = order_storage_list[i][3]
        var rowCost = parseFloat(order_storage_list[i][1])*parseInt(rowquant);
        
        var tablerowdata = document.createElement('tr');
        
        var index_field = document.createElement('th');
        index_field.textContent = i+1;
        tablerowdata.appendChild(index_field);
        
        var name_field = document.createElement('td');
        name_field.textContent = rowname;
        tablerowdata.appendChild(name_field);

        var quantity_field = document.createElement('td');
        quantity_field.textContent =  rowquant;
        tablerowdata.appendChild(quantity_field);    
        
        var cost_field = document.createElement('td');
        cost_field.textContent = rowCost;  
        tablerowdata.appendChild(cost_field)

        var rm_button_td = document.createElement('td')

        var rm_button = document.createElement('button')
        rm_button.setAttribute('class', 'btn btn-danger remove_order_item')
        rm_button.textContent = "remove"
        rm_button_td.appendChild(rm_button)
        tablerowdata.appendChild(rm_button_td)

        new_tablebody.appendChild(tablerowdata);
    }
    
    tablebody.innerHTML = new_tablebody.innerHTML
}

function findNameInList(listObject, searchName){
    let isNameFound = false;
    let indexFound = -1;

    for (var i = 0; i < listObject.length; i++) {
    if(listObject[i][0] === searchName) {
        isNameFound = true;
        indexFound = i;
        break;
    }
    }
    return indexFound;
}

const order_tableButton = document.getElementById("OrderDiv")
order_tableButton.addEventListener('click', function(event) {
    // Check if the clicked element is a button
    if (event.target.classList.contains('remove_order_item')) {
        var clickedButton = event.target;
        var clickedRow = clickedButton.closest('tr');
        var clicked_row_td = clickedRow.getElementsByTagName("td");
        

        var clickedOrderProductName = clicked_row_td[0].textContent
        var index = findNameInList(order_storage_list, clickedOrderProductName);
        var removed_index = order_storage_list.splice(index, 1);
        editOrderList();
    }
    })

const sellButton = document.getElementById("SellOrdersButton")

sellButton.addEventListener('click', function() {
    const sellForm = document.getElementById("sellForm")
    var sellform_inputs = sellForm.getElementsByTagName("input")
    
    for(let i=0; i<order_storage_list.length; i++){
        var sell_params = order_storage_list[i];
        sellform_inputs[1].value = sell_params[2]
        sellform_inputs[2].value = current_order_id;
        sellform_inputs[3].value = sell_params[3]
        

    }
    
    order_storage_list = []
    
})