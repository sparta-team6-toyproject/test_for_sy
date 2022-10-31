let input_list = [];
function save_input(val) {
  let tag = $(val).val();
  input_list.push(tag);
  $("#input").val(input_list);
}

function search() {
  let search_list = $("#input").val();
  console.log(search_list);
  $.ajax({
    type: "POST",
    url: "/honeymoon",
    data: { search_give: search_list },
    success: function (response) {
      alert(response["msg"]);
      window.location.reload();
    },
  });
}
