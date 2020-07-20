#include <stdio.h>
#include <limits.h>
#include <float.h>
#include <string.h>
#include "Node.h" //Nodes amd Edges
#define INF DBL_MAX

int main(int argc, char *argv[]) {
	Node node_data; //head is unique
	node_data.x = node_data.y = -INF;
	node_data.next = NULL;

	Edge edge_data; //head of the linked list (unique)
	edge_data.begins_at = edge_data.ends_at = NULL;
	edge_data.next = NULL;

	FILE *fp = fopen(argv[1], "r");
	int BUFSIZE = 99;
	char buff[BUFSIZE];

	while(fgets(buff, BUFSIZE - 1, fp) != NULL) {
		if (buff[0] != '\n') {
			Node* last_node = &node_data;
			while (last_node->next != NULL) 
				last_node = last_node->next;
			double x, y;
			sscanf(buff, "%lf %lf", &x, &y);
			Node* new_node = add_node(&node_data, x, y);
			if (last_node != &node_data) {
				add_edge(&edge_data, last_node, new_node);
			}
		} else {
			Node* last_node = &node_data;
			while (last_node->next != NULL)
				last_node = last_node->next;
			add_edge(&edge_data, last_node, edge_data.next->begins_at);
		}
	}
	fclose(fp);
	return 0;
}
