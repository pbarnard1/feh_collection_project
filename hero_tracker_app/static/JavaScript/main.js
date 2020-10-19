$('document').ready(function() {
    if (document.getElementById('user_heroes') != null) {
        var heroData = JSON.parse(document.getElementById('user_heroes').textContent);
        var $tableName = $('.hero_table');
    } else if (document.getElementById('all_heroes') != null) {
        var heroData = JSON.parse(document.getElementById('all_heroes').textContent);
        var $tableName = $('.new_hero_table');
    }
    console.log("Hero data: ",heroData)
    $tableName.bootstrapTable({
        pagination: true,
        search: true,
        sortReset: true,
        rowStyle: "rowStyle",
        showColumns: true,
        showColumnsToggleAll: true,
        toolbar: ".my-toolbar",
        columns: [{
            field: 'hero',
            sortable: true,
            title: 'Hero',
        }, {
            field: 'movement',
            sortable: true,
            title: 'Movement',
        }, {
            field: 'weapon',
            sortable: true,
            title: 'Weapon',
        }, {
            field: 'color',
            sortable: true,
            title: 'Color',
        }, {
            field: 'debut_date',
            sortable: true,
            title: 'Debut',
        }, {
            field: 'hp',
            sortable: true,
            title: 'HP',
        }, {
            field: 'atk',
            sortable: true,
            title: 'ATK',
        }, {
            field: 'spd',
            sortable: true,
            title: 'SPD',
        }, {
            field: 'def',
            sortable: true,
            title: 'DEF',
        }, {
            field: 'res',
            sortable: true,
            title: 'RES',
        }],
        data: heroData,
    });
    console.log("Table made")
});

function rowStyle(row, index) {
    console.log("Getting colors for row " + index)
    if (row.color == "Red") {
        //console.log("Red")
        return {
            classes: 'red',
            css: {
                'background-color': '#db4d75',
            }
        };
    } else if (row.color == "Blue") {
        //console.log("Blue")
        return { 
            classes: 'blue',
            css: {
                'background-color': '#4ea3f2',
            }
        }
    } else if (row.color == "Green") {
        //console.log("Green")
        return { 
            classes: 'green',
            css: {
                'background-color': '#63d13f',
            }
        }
    } else {
        //console.log("Colorless")
        return { 
            classes: 'colorless',
            css: {
                'background-color': '#989cb8',
            }
        }
    }
}