A = readtable('Matriceok.xlsx','Range','B2:AG33')
% A = [0 0 1 0;0 0 1 1;1 1 0 0;0 1 0 0];
D = diag(sum(A))
% D = [1 0 0 0;0 2 0 0;0 0 2 0;0 0 0 1];
L = D-A
[vect, val] = eig(L)


fiedler = vect(:,2)

[a,b] = sort(fiedler)