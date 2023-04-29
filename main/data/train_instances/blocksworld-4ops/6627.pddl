

(define (problem BW-rand-7)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 )
(:init
(arm-empty)
(on b1 b6)
(on b2 b4)
(on b3 b7)
(on-table b4)
(on b5 b2)
(on b6 b3)
(on b7 b5)
(clear b1)
)
(:goal
(and
(on b1 b6)
(on b2 b7)
(on b3 b5)
(on b5 b4))
)
)


