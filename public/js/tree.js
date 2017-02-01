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

/** Function when init
*/
currentNode = null;
init = function(){
    svg = d3.select('#tree').append('svg').style('height','100%').style('width','100%').append('g').attr("transform", "translate(" + 100 + "," + 50 + ")");;

    tree = d3.layout.tree().size([600,1000]);
    diagonal = d3.svg.diagonal().projection(function(d){return [d.y, d.x];});
    i = 0;
    currentNode = treeData;
    update(treeData);
}

/** Update function
*/
update = function(source,root){
    
    nodes = tree.nodes(root?root:source);
    edges = tree.links(nodes);
    updateNodes(nodes,source);
    updateEdges(edges,source);

    nodes.forEach(function(d){
      d.x0=d.x;
      d.y0=d.y;
    });
}

updateNodes = function(nodes, source){
    // Node update
    node = svg.selectAll('g.node').data(nodes, function(d){ return d.id || (d.id = ++i);});

    // Node enter
    nodeEnter = node.enter().append('g')
      .attr('class','node')
      .attr("transform",function(d){ return "translate(" + source.y0 + "," + source.x0 + ")";});

    nodeEnter.append("text")
        .attr("x", 0)
        .attr("y", -10)
        .text(function(d) { return d.name; })
        .on("click",function(d){
          if(d.children){
            d._children = d.children;
            d.children=null;
          } else {
            d.children = d._children;
            d._children = null;
          }
          update(d,currentNode);
        });

    nodeEnter.append("text")
        .style("cursor","pointer")
        .attr("x", 10)
        .attr("y",10)
        .attr("text-anchor","end")
        .text(function(d) { return "back"; })
        .on("click", function(d){ 
          currentNode=d.parent;
          update(d.parent);
        });
    nodeEnter.append("text")
        .style("cursor","pointer")
        .attr("x", 20)
        .attr("y",10)
        .attr("text-anchor","start")
        .text(function(d) { return "go"; })
        .on("click", function(d){ 
          currentNode=d;
          update(d);
        });
        

    node.transition().duration(1000).attr("transform", function(d) {console.log(d); return "translate(" + d.y + "," + d.x + ")"; });

    nodeExit = node.exit().transition().duration(1000).attr("transform",function(d){return "translate(" + source.y + ","+source.x + ")"; }).remove();

    nodeExit.select("text").style("fill-opacity",0);

}
updateEdges = function(edges, source){
  edge = svg.selectAll("path.edge").data(edges, function(d){ return d.target.id; });

  edge.enter().insert("path","g")
    .attr("class","edge")
    .attr("d",function(d){ var parentPosition = {x: source.x0, y: source.y0};
    return diagonal({source: parentPosition, target: parentPosition}); })
    .style("fill","none")
    .style("stroke","#000");
  edge.transition().duration(1000).attr("d",diagonal);

  edge.exit().transition().duration(1000)
    .attr("d",function(d){var parentPosition = {x:source.x,y:source.y};
    return diagonal({source: parentPosition, target: parentPosition}); }).remove();
}



/** Things to learn use api */
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
