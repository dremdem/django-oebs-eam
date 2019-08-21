$(function () {
    console.log($('#id_root_asset').val());
    $('#container').jstree({
        'core': {
            'data': {
                "url": "/asset_tree/" + root_asset,
                "dataType": "json" // needed only if you do not supply JSON headers
            }
        }
    });
});


$(document).ready(function () {
    let table = $('#table_id').DataTable({
        "ajax": '/parameters',
        "columns": [
            {'data': 'name'},
            {'data': 'value'},
            {
                "data": null,
                "defaultContent": '<button type="button" class="btn btn-info">Edit</button>'
            }
        ],
        'paging': false,
        'searching': false,
        "info": false,
    });
    $('#table_id tbody').on('click', 'button', function () {
        let data = table.row($(this).parents('tr')).data();
        $('#name').val(data['name']);
        $('#value').val(data['value']);
        if (data['name'] === "root_asset") {
            $("#raModal").modal();
        } else {
            $("#ishModal").modal();
            if(!data['value'])
                $("#is_sync").prop("checked", false);
            else
                $("#is_sync").prop("checked", true);
        }
    });
});

$('#ish_form').on('submit', function (e) {
    e.preventDefault();
    let $this = $(this);
    let type = $('#type').val();
    let method = '';
    let url = '/set_sync';
    method = 'POST';

    $.ajax({
        url: url,
        method: method,
        success: function (data, textStatus, jqXHR) {
            location.reload();
        },
        data: $this.serialize()
    });
});


$('#ra_form').on('submit', function (e) {
    e.preventDefault();
    let $this = $(this);
    let type = $('#type').val();
    let method = '';
    let url = '/set_root_asset';
    method = 'POST';

    $.ajax({
        url: url,
        method: method,
        success: function (data, textStatus, jqXHR) {
            location.reload();
        },
        data: $this.serialize()
    }).error(function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR)
    });
});