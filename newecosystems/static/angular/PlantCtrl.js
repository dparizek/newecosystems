(function () {
    'use strict';
    var newecosystems = angular.module('newecosystems');

    newecosystems.controller('PlantCtrl', function ($scope, $filter, $state, $sce, Restangular, PlantsForGrid, _) {
        $scope.plantSelection = [];

        PlantsForGrid.getList().then(function (plants) {
            $scope.plantList = plants;
        });

        $scope.character_forbtotree = true;
        $scope.character_annualness = true;
        $scope.character_waterneeds = true;
        $scope.character_commonality = true;
        $scope.charactersUsed = "";

        $scope.pruning_method = 'pairwise';
        $scope.numberResults = 17;
        $scope.prunedResults = [];
        $scope.resultEdges = [];
        $scope.mstReport = [];

        $scope.filterOptions = {
            filterText: ''
        };

        $scope.plantListGrid = {
            data: 'plantList',
            filterOptions: $scope.filterOptions,
            columnDefs: [
                {field: 'habit', displayName: 'Habit', width: '100px'},
                {field: 'common_name', displayName: 'Common Name', width: '150px'},
                {field: 'genus', displayName: 'Genus', width: '100px'},
                {field: 'species', displayName: 'Species', width: '100px'},
                {field: 'family', displayName: 'Family', width: '100px'},
                {field: 'annualness_index', displayName: 'Annualness Index', width: '140px'},
                {field: 'forb_to_tree_index', displayName: 'Forb to Tree Index', width: '140px'},
                {field: 'water_needs_index', displayName: 'Water Needs Index', width: '140px'},
                {field: 'commonality_index', displayName: 'Commonality Index', width: '140px'},
                {field: 'flower_spring', displayName: 'Flower Spring', width: '140px'},
                {field: 'flower_summer', displayName: 'Flower Summer', width: '140px'},
                {field: 'flower_fall', displayName: 'Flower Fall', width: '140px'},
                {field: 'flower_winter', displayName: 'Flower Winter'}
            ],
            selectedItems: $scope.plantSelection,
            showSelectionCheckbox: true,
            sortInfo: {fields: ['common_name'], directions:['asc']},
            enableColumnResize: true
        };

        $scope.fieldInvalid = function (form, field) {
            if ($scope[form][field]) {
                var fieldErrors = $scope[form][field].$error;
                if (fieldErrors.required) {
                    return true;
                } else if (fieldErrors.maxlength) {
                    return true;
                } else if (fieldErrors.number) {
                    return true;
                } else if (fieldErrors.min) {
                    return true;
                } else if (fieldErrors.max) {
                    return true;
                } else {
                    return false;
                }
            }
        };

        $scope.readyGetList = function () {
            if (!$scope.plantListForm.$invalid && $scope.plantSelection[0]) {
                return true;
            } else {
                return false;
            }
        };

        $scope.getMST = function (edges, N) {
            // ----------------------------
            // Kruskal method for calculating LeastBranchingTree:
            // Calculate the lengths of all edges.
            // Order from smallest to largest.
            // Choose first 2 edges.
            // Examine edge 3 and add it iff one or both of its nodes is not part of either of the first 2 edges.
            // Examine edge 4 and add it iff one or both of its nodes is not part of any of the previously added edges.
            // Examine edge 5 and add it iff one or both of its nodes is not part of any of the previously added edges.
            // ...
            // Stop when the tree contains N-1 edges. This constitutes the LBT.
            // --------------------------------------
            // Kruskal method for calculating LeastBranchingTree:
            // Calculate the lengths of all edges.
            // Order from smallest to largest.
            // Choose first edge - add both nodes.
            // Examine edge 2 and add it if one and only one node is not part of either of the first edge.
            // Examine edge 3 and add it if one and only one node is not part of any of the previously added edges.
            // Examine edge 4 and add it if one and only one node is not part of any of the previously added edges.
            // ...
            // Stop when the tree contains N-1 edges. This constitutes the LBT.
            // _____________________________________________________

            var mstEdges = [];
            var mstNodes = [];

            // console.log("IN edges = ");
            // console.log(edges );
            // console.log("IN N = " + N);
            // console.log("IN edges.length = " + edges.length);
            //sort edges by edge length ascending
            var sortedEdges = _.sortBy(edges, function (edge) { return edge[2]; });
            // console.log("sorted edges = ");
            // console.log(sortedEdges );
            //choose first edges, add it's nodes
            var edge = sortedEdges[0];
            mstNodes.push(edge[0]);
            mstNodes.push(edge[1]);
            mstEdges.push(edge);
            var counter = 0;
            while (counter < sortedEdges.length) {
                console.log("counter = " + counter);
                edge = sortedEdges[counter];
                if (edge === undefined) {
                    console.log("ERROR: undefined edge found:");
                    console.log(edge);
                    // console.log("sortedEdges[0]");
                    // counteronsole.log(sortedEdges[counter]);
                }

                var species1 = edge[0];
                var species2 = edge[1];
       
                //if only one plant in this edge is a new one, add it to our list of nodes and add the edge
                if (!_.contains(mstNodes, species1) && _.contains(mstNodes, species2)) {
                    if (mstEdges.length < N - 1) {
                        mstEdges.push(edge);
                        mstNodes.push(species1);
                        counter = 0;
                        //console.log("push sp1 mstEdges.length = " + mstEdges.length);
                    } else {
                        break;
                    }
                } else if (!_.contains(mstNodes, species2) && _.contains(mstNodes, species1)) {
                    if (mstEdges.length < N - 1) {
                        mstEdges.push(edge);
                        mstNodes.push(species2);
                        counter = 0;
                        //console.log("push sp2 mstEdges.length = " + mstEdges.length);
                    } else {
                        break;
                    }
                }
                counter ++;
            }
            // console.log("OUT mstEdges.length = " + mstEdges.length);
            // console.log("OUT mstEdges = ");
            // console.log(mstEdges);
            return mstEdges;
        };

        var mstReporter = function (mst) {
            $scope.mstReport = [];
            for (var i=0; i < mst.length; i++) {
                var thisMST = mst[i][0] + ", " + mst[i][1] + ", " + mst[i][2] + ";";
                $scope.mstReport.push(thisMST);
            }
        };

        $scope.strikebatch = function (mst) {
            // ----------------------
            // */StrikeBatches to prune an LBT from N nodes to S nodes:
             
            // Calculate least branching tree (LBT) --- see below.
            // Order LBT's edges by length (LONGEST first)
            // Strike SHORTER half of the edges. [If LBT has an odd number of edges, x, strike the shortest (x - 1)/2]
            // Recalculate LBT of the remaining (LONGER) half
            // Re-order (LONGEST first)
            // Strike SHORTER half of these.
            // Repeat the loop until LBT contains fewer than 2S edges (where S is the number desired in the set).
            // Use S-1 LONGEST edges remaining.
            // Return the list of nodes attached to these edges.
            
            var numberDesired = $scope.numberResults;
            // console.log("numberDesired = " + numberDesired);
            var cutoff = numberDesired * 2;
            // console.log("cutoff: " + cutoff);
    
            var leftoverNodes = [];
            var sortedEdges = [];
            var prunedEdges = [];

            while (mst.length > cutoff) {
                $scope.N = Math.floor($scope.N / 2);
                // console.log("next N = " + $scope.N);
                sortedEdges = _.sortBy(mst, function (edge) { return -edge[2]; });
                var halfPoint = Math.floor(sortedEdges.length / 2);
                prunedEdges = sortedEdges.slice(0, halfPoint);
                mst = $scope.getMST(prunedEdges, $scope.N);
                //console.log("length of MST returned inside while loop of strike batches: " + mst.length );
            
            }
            
            //now that fewer than 2 * S (S = number of desired species in final pruned list) connected in LBT, 
            /// we use the S-1 longest edges remaining
            //so resort
            sortedEdges = _.sortBy(mst, function (edge) { return -edge[2]; });
            //now we need just the S-1 edges
            prunedEdges = sortedEdges.slice(0, numberDesired - 1);

            // console.log("S-1 edges length = " + prunedEdges.length);
            // console.log("so remaining S-1 edges are: ");
            // console.log(prunedEdges);

            // Return the list of nodes attached to these edges.
            leftoverNodes = [];
            for (var y in prunedEdges) {
                var species1_id = prunedEdges[y][0];
                var species2_id = prunedEdges[y][1];
                // console.log("species1_id = " + species1_id);
                // console.log("species2_id = " + species2_id);
                leftoverNodes.push(species1_id);
                leftoverNodes.push(species2_id);
                $scope.resultEdges.push(species1_id + ", " + species2_id + ", " + prunedEdges[y][2] + ';');
                leftoverNodes = _.uniq(leftoverNodes);
            }
            return leftoverNodes;
        };

        $scope.pairwise = function (edges) {
            var prunedPlantList = [];
            var numberOfSpecies = $scope.numberResults;
            // console.log("number Of Species Desired:");
            // console.log(numberOfSpecies);
         
            //order branches by length
            var sortedEdges = _.sortBy(edges, function (edge) { return -edge[2]; });
            // console.log("sortedEdges in Pairwise:");
            // console.log(sortedEdges);
            
            //choose the longest
            var species1 = sortedEdges[0][0];
            var species2 = sortedEdges[0][1];
            prunedPlantList.push(species1);
            prunedPlantList.push(species2);
            $scope.resultEdges.push(species1 + ", " + species2 + ", " + sortedEdges[0][2] + ';');

            //iteratively choose next longest edge that adds two species, until x number of species are in suite
            var inputPlantNumber = $scope.plantSelection.length;
            for (var i = 1; i < sortedEdges.length; i++) {
                var nextLongest = sortedEdges[i];
                //does it add two new species?
                species1 = nextLongest[0];
                species2 = nextLongest[1];
                var yes1 = _.contains(prunedPlantList, species1);
                var yes2 = _.contains(prunedPlantList, species2);

                if (!yes1 && !yes2) {
                    // console.log("prunedPlantList:");
                    // console.log(prunedPlantList);
                    //it does add 2 new species, so add those species to the list
                    prunedPlantList.push(species1);
                    $scope.resultEdges.push(species1 + ", " + species2 + ", " + sortedEdges[0][2] + ';');
                    if (prunedPlantList.length >= numberOfSpecies) {
                        break;
                    }
                    prunedPlantList.push(species2);
                    if (prunedPlantList.length >= numberOfSpecies) {
                        break;
                    }
                }
            }
            return prunedPlantList;
        };

        $scope.getPrunedPlantList  = function () {
            //need the nodes and edges to build the MST
            $scope.prunedResults = "";
            $scope.charactersUsed = "";
            $scope.resultEdges = [];

            var plants = [];
            var nodes = [];
            var edges = [];
            var numCharacters = 0;

            //get nodes, and get plants into an array
            for (var key in $scope.plantSelection) {
                //console.log(key, $scope.plantSelection[key]);
                if ($scope.plantSelection.hasOwnProperty(key)) {
                    var thisPlant = $scope.plantSelection[key];
                    nodes.push("P" + thisPlant.id);
                    plants.push(thisPlant);
                }
            }
            //console.log("Number of plants (N) = " + plants.length);
            //now get edges
            for (var i = 0; i < plants.length; i++) {
                var fromNode = String(plants[i].id);
                for (var j = i + 1; j < plants.length; j++) {
                    var toNode = String(plants[j].id);
                    var thisEdge = [];
                    if (fromNode != toNode) {
                        var sumOfSquares = 0;
                        thisEdge.push("P" + fromNode);
                        thisEdge.push("P" + toNode);
                        //now calculate the edge distance
                        var thisDiff = 0;
                        var thisSquare = 0;
                        if ($scope.character_forbtotree === true) {
                            thisDiff = plants[i].forb_to_tree_index - plants[j].forb_to_tree_index;
                            thisSquare = Math.pow(thisDiff, 2);
                            sumOfSquares = sumOfSquares + thisSquare;
                        }
                        if ($scope.character_waterneeds === true) {
                            thisDiff = plants[i].water_needs_index - plants[j].water_needs_index;
                            thisSquare = Math.pow(thisDiff, 2);
                            sumOfSquares = sumOfSquares + thisSquare;
                        }
                        if ($scope.character_commonality === true) {
                            thisDiff = plants[i].commonality_index - plants[j].commonality_index;
                            thisSquare = Math.pow(thisDiff, 2);
                            sumOfSquares = sumOfSquares + thisSquare;
                        }
                        if ($scope.character_annualness === true) {
                            thisDiff = plants[i].annualness_index - plants[j].annualness_index;
                            thisSquare = Math.pow(thisDiff, 2);
                            sumOfSquares = sumOfSquares + thisSquare;
                        }

                        var mahanolobisDistance = Math.sqrt(sumOfSquares);
                        thisEdge.push(mahanolobisDistance);
                    }
                    edges.push(thisEdge);
                }
            }

            //next we feed the nodes and edges to MST (LBT) calculator
            //var mst = $scope.kruskal(nodes, edges);
            $scope.N = plants.length;
            var mst = $scope.getMST(edges, $scope.N);
            mstReporter(mst);
            //prune the list
            var prunedList = [];
            if ($scope.pruning_method == 'pairwise') {
                prunedList = $scope.pairwise(edges);
            } else if ($scope.pruning_method == 'strikebatch') {
                prunedList = $scope.strikebatch(mst);
            }
            var output = [];
            for (var x in prunedList) {
                var newResult = {};
                newResult.id = prunedList[x].slice(1);
                var currentPlant = _.find(plants, function (plant) { return plant.id == newResult.id; });
                newResult.firefly_url = currentPlant.firefly_url;
                newResult.common_name = currentPlant.common_name;

                output.push(newResult);
            }
            $scope.prunedResults = output;
            if ($scope.character_forbtotree === true) {
                $scope.charactersUsed += "Habit, ";
            }
            if ($scope.character_annualness === true) {
                $scope.charactersUsed += "Longevity, ";
            }
            if ($scope.character_commonality === true) {
                $scope.charactersUsed += "Commonality, ";
            }
            if ($scope.character_waterneeds === true) {
                $scope.charactersUsed += "Water Needs, ";
            }
            var removeCommaPos = $scope.charactersUsed.length - 2;
            $scope.charactersUsed = $scope.charactersUsed.substring(0, removeCommaPos);

        };

    });

}());




