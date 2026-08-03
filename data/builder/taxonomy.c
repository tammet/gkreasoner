/*
 * Taxonomy lookup table
 *
 * Reference implementation
 *
 * Table layout (size in words, i.e. 64- or 32-bit ints):
 * |------|------------------------|
 * | size | data                   |
 * |------|------------------------|
 * |    1 | table size             |  (on disk only, not in memory)
 * |------|------------------------|
 * |    1 | number of classes n    |
 * |------|------------------------|
 * |    n | index to class 0..n-1  |
 * |------|------------------------|
 * |    1 | number of parents p    |  \
 * |------|------------------------|   > repeated blocks for each class
 * |    p | index to parent 0..p-1 |  /
 * |------|------------------------|
 *
 * Taxonomy graph has topological sort defined:
 *      parent class number < child class number
 * and  parent table index < child table index
 *
 * Principle of searching the taxonomy graph
 *  (already implemented by this file):
 * 1. look up the index of start node (idx1)
 * 2. look up the index of goal node (idx2)
 * 3. start the search from table[idx1] by expanding each parent
 *       (table[parent1], table[parent2], ...)
 * 4. until one of the parents == idx2 or there are no more parents to expand
 *
 * usage:
 *   unsigned int *tbl = load_taxonomy("filename.dat");
 *   unsigned int *queue = prep_queue(tbl);
 *   int is_higher = is_more_general(45672, 1134, tbl, queue);
 *
 * numeric identifiers come from e.g. default logic rules
 */


#include <stdio.h>
#include <stdlib.h>

/*
 * Read taxonomy table from a file.
 * Allocates memory size given on the first line of the input file
 * caller is expected to free(tbl);
 */
unsigned int *load_taxonomy(char *filename) {
    FILE *f = NULL;
    size_t i, sz;
    unsigned int *tbl = NULL;

    if((f = fopen(filename, "r")) == NULL) {
        fprintf(stderr, "Failed to open taxonomy file\n");
        return NULL;
    }

    if(fscanf(f, "%lu\n", &sz) != 1) {
        fprintf(stderr, "Failed to read taxonomy size\n");
        fclose(f);
        return NULL;
    }

    tbl = malloc(sz * sizeof(unsigned int));
    if(!tbl) {
        fprintf(stderr, "Failed to allocate taxonomy table\n");
        fclose(f);
        return NULL;
    }

    for(i=0; i<sz; i++) {
        unsigned int v;
        if(feof(f) || fscanf(f, "%u\n", &v) != 1) {
            fprintf(stderr, "Failed to read taxonomy file\n");
            fclose(f);
            free(tbl);
            return NULL;
        }
        tbl[i] = v;
    }

    fclose(f);
    return tbl;
}

/*
 * Prepare re-usable queue for taxonomy searches
 * we will never search more nodes than tbl[0]
 * caller is expected to free(queue);
 */
unsigned int *prep_queue(unsigned int *tbl) {
    unsigned int *queue = malloc(tbl[0] * sizeof(unsigned int));
    if(!queue) {
        fprintf(stderr, "Failed to allocate queue\n");
        return NULL;
    }
    return queue;
}

/*
 * Breadth first search for taxonomy graphs
 * uses a predefined topological sort to prune parents
 * that do not lead to goal node
 * queue must be prepared with prep_queue()
 */
int bfs(unsigned int class1, unsigned int class2, unsigned int *tbl,
                                                    unsigned int *queue) {
    size_t head = 0;
    size_t tail = 1;
    unsigned int goal = tbl[class2 + 1];
    queue[0] = tbl[class1 + 1];

    //printf("\nCP20\n");                                                        
    while(head < tail) {
        //printf("\nCP21\n");
        unsigned int curr = queue[head++];
        size_t i = curr + 1;
        size_t p = curr + tbl[curr];
        //printf("\nCP22\n");
        for(; i<=p; i++) {
            //printf("\nCP23\n");
            unsigned int parent = tbl[i];
            if(parent == goal) {
                return 1;
            } else if(parent > goal) {
                if(tail >= tbl[0]) {
                    fprintf(stderr, "Graph is cyclic or corrupt\n");
                    return 0;
                }
                queue[tail++] = parent;
            }
        }
        //printf("\nCP24\n");
    }
    //printf("\nCP25\n");
    return 0;
}

/*
 * Taxonomy search
 *
 * returns 1 if class2 is more general than class1
 * returns 0 otherwise
 *
 * example:
 *     class1 = penguin  class2 = bird  : 1
 *     class1 = mammal   class2 = bear  : 0
 */
int is_more_general(unsigned int class1, unsigned int class2, unsigned int *tbl,
                                                    unsigned int *queue) {
    //printf("\nCP30\n");                                                      
    if(class1 <= class2) {
        //printf("\nCP31\n");
        return 0;
    }
    //printf("\nCP33 class1 %d class2 %d tbl %d queue %d\n",class1,class2,(unsigned int)tbl,(unsigned int)queue);
    return bfs(class1, class2, tbl, queue);
    //printf("\nCP34\n");
}

