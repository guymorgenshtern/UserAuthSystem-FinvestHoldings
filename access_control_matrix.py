#implementation of RBAC access control using a matrix 
class AccessControlMatrix:
    permissions_by_object_subject_matrix = {}

    def __init__(self) -> None:
         self._build_matrix('matrix.txt')
        
    
    def _build_matrix(self, file_name):
            #open txt representation of matrix
            with open(file_name, 'r', newline='\n', encoding='utf-8') as file:
                matrix = file.read()
            print(matrix)

            #splitting csv data into header: defines objects, data: defines subjects and permissions
            rows = [row.split(",") for row in matrix.strip().split("\n")]
            header = rows[0][0:]
            data = rows[1:]
            print(rows)
    

            #converting txt to nested dictionary: dict[subject][object] = T/F based on permissions defined in csv ('X' = T)        
            for i in range(len(data)):
                self.permissions_by_object_subject_matrix[data[i][0]] = {}
                for j in range(1, len(header) + 1):
                    print(data[i][0] + " " + header[j - 1]+ " " + str(len(data[i])))
                    self.permissions_by_object_subject_matrix[data[i][0]][header[j - 1]] = True if data[i][j] == "X" else False
        
    def to_string(self) -> str:
        first_dimension_keys = list(self.permissions_by_object_subject_matrix.keys())
        second_dimension_keys = list(self.permissions_by_object_subject_matrix[first_dimension_keys[0]].keys())

        s = ""
        for first_key in first_dimension_keys:
            for second_key in second_dimension_keys:
                s += (f"dict['{first_key}']['{second_key}']: {self.permissions_by_object_subject_matrix[first_key][second_key]}\n")
        
        return s

    def check_permission(self, subject, object):
        return self.permissions_by_object_subject_matrix[subject][object]
