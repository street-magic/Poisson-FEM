#include <stdio.h>
#include <limits.h>
#include <float.h>
#include <string.h>
#include <stdbool.h>
#include "Node.h" //Nodes and Edges
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

	bool python = true;

	Node* first_cont_node = NULL;
	while(fgets(buff, BUFSIZE - 1, fp) != NULL) {
		if (buff[0] != '\n') {
			Node* last_node = &node_data;
			while (last_node->next != NULL) 
				last_node = last_node->next;

			double x, y;
			sscanf(buff, "%lf %lf", &x, &y);
			Node* new_node = add_node(&node_data, x, y);
			if (first_cont_node == NULL){
				first_cont_node = new_node;
			} else {
				add_edge(&edge_data, last_node, new_node);
			}
		} else {
			//printf("closing edge\n");
			Node* last_node = first_cont_node;
			while (last_node->next != NULL)
				last_node = last_node->next;
			//printf("%lf %lf\n", last_node->x, last_node->y);
			add_edge(&edge_data, last_node, first_cont_node);
			first_cont_node = NULL;
		}
	}
	fclose(fp);

	Edge* cur_edge = edge_data.next;
	while (cur_edge != NULL) {
		if (python) {
			printf("plt.plot([%lf,%lf],",cur_edge->begins_at->x, cur_edge->ends_at->x);
			printf("[%lf,%lf],'k-')\n",cur_edge->begins_at->y, cur_edge->ends_at->y);
		}
		cur_edge = cur_edge->next;
	}
	return 0;
}
