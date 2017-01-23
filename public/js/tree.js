treeData = {
    "name": "Top Level",
        "children": [
        {
            "name": "Level 2: A",
            "children": [
                {"name": "Level 3A: A",},
                {"name": "Level 3A: B",}
            ]
        },
        {
            "name": "Level 2: B",
            "children": [
                {
                    "name": "Level 3B: A",
                    "children": [
                    {
                        "name": "Level 4BA: A",
                        "children": [
                        {
                            "name": "Level 5BAA: A",
                            "children": [
                            {"name": "Level 6BAAA: A", "size": 3938},
                            {"name": "Level 6BAAA: B", "size": 3938},
                            {"name": "Level 6BAAA: C", "size": 3938},
                            ]
                        },
                        {
                            "name": "Level 5BAA: B",
                            "children": [
                            {"name": "Level 6BAAB: A", "size": 3534},
                            {"name": "Level 6BAAB: B", "size": 3534},
                            {"name": "Level 6BAAB: C", "size": 3534},
                            ]
                        },
                        {
                            "name": "Level 5BAA: C",
                            "children": [
                            {"name": "Level 6BAAC: A", "size": 3534},
                            ]
                        }
                        ]
                    },
                    ]
                }]
        },
        {
            "name": "Level 2: C",
            "children": [
                {
                    "name": "Level 3C: A",
                    "children": [
                    {
                        "name": "Level 4CA: A",
                        "children": [
                            {"name": "Level 5CAA: A",},
                            {"name": "Level 5CAA: B",},
                            {"name": "Level 5CAA: C",}
                        ]
                    },
                    ]
                },
                {
                    "name": "Level 3C: B",
                    "children": [
                    {
                        "name": "Level 4CB: A",
                        "children": [
                            {"name": "Level 5CBA: A",},
                            {"name": "Level 5CBA: B",},
                            {"name": "Level 5CBA: C",}
                        ]
                    },
                    {
                        "name": "Level 4CB: B",
                        "children": [
                            {"name": "Level 5CBB: A",},
                            {"name": "Level 5CBB: B",},
                            {"name": "Level 5CBB: C",}
                        ]
                    },
                    ]
                }
                ]
        }
        ]
};
window.onload = function(){init();}
init = function(){
    svg = d3.select('#tree').append('svg').style('height','100%').style('width','100%').append('g').attr("transform", "translate(" + 100 + "," + 50 + ")");;

    tree = d3.layout.tree().size([600,500]);
    diagonal = d3.svg.diagonal().projection(function(d){return [d.y, d.x];});
    i = 0;
    update(treeData);
}
update = function(source){
    nodes = tree.nodes(source);
    links = tree.links(nodes);

    node = svg.selectAll('g.node').data(nodes, function(d){ return d.id || (d.id = ++i);});
    nodeEnter = node.enter().append('g').attr('class','node');
    nodeEnter.append("text")
        .attr("x", function(d) { return d.children || d._children ? -10 : 10; })
        .attr("dy", ".35em")
        .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
        .text(function(d) { return d.name; })
    node.attr("transform", function(d) {console.log(d); return "translate(" + d.y + "," + d.x + ")"; });

}

const initCircle = function(){
    svg = d3.select("body").append("div").append("svg").attr("height",400).style("width","100%");
    /* canvas = d3.select("#tree")
                .append("svg")
                .attr("width",400)
                .attr("height",400);
    
    diagonal = d3.svg.diagonal(); */
}
circleData=[10,10,10,10,10,10,10];
updateCircle = function(){
     if(circleData.length==0){ sum=1;}else{sum = circleData.reduce(function(a,b){ return a+b;});}
     width = Number(svg.style('width').replace('px',''));

     selection = svg.selectAll('circle').data(circleData);
     lastcx=0;
     
     selection.attr('cy',200).transition().duration(1000).attr('cx',function(d,i){ r=radius(d,width,sum); cx = lastcx+r; lastcx=cx+r; return cx;}).transition().duration(1000).attr('r', function(d){ return radius(d,width,sum);});

     selectionEnter = selection.enter().append('circle').attr('cy',200).attr('cx',function(d,i){ r=radius(d,width,sum); cx = lastcx+r; lastcx=cx+r; return cx;}).attr('r', function(d){ return radius(d,width,sum);}).on('click',function(d,i){circleData.splice(i,1); updateCircle();});

    selectionExit = selection.exit().transition().attr('r',0).remove();

}
radius = function(d,width,sum){
    return d*width/(sum*2);
}
new_data = function(){
    input = document.getElementById('new-data');
    circleData.push(Number(input.value));
    updateCircle();
}
