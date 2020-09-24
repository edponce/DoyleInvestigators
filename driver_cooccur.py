from gutenberg import *


# Example of expected format of data that the method needs
rows_example = ['Holmes', 'Watson', 'criminal', 'treasure', 'man', 'poison', 'killed']

columns_example = ["P. Moriarty", "T. Baldwin", "J. Hope","J. Small","Tonga","J. Stapleton","J. Turner"]
data_example = [[1,1,0,0,0,0,0],[0,0,0,0,1,0,0],[1,1,0,0,0,1,0],[0,0,0,1,1,0,0],[0,0,0,1,0,0,1],[0,0,0,0,1,0,0],[0,0,0,0,2,0,0]]

# Plot
visualize_co_occurrence(data_example,rows_example,columns_example)
plt.show()
