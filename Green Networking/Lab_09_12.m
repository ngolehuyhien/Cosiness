% A = [0 0 1 0;0 0 1 1;1 1 0 0;0 1 0 0];
% G= []
A = G+G'
D = diag(sum(A))

[V,D] = eig(A)
L = D-A
[vect, val] = eig(L)

fiedler = vect(:,2)
[a,b] = sort(fiedler)