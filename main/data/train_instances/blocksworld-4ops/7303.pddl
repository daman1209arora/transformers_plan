

(define (problem BW-rand-7)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 )
(:init
(arm-empty)
(on-table b1)
(on b2 b5)
(on b3 b7)
(on b4 b1)
(on b5 b3)
(on-table b6)
(on b7 b4)
(clear b2)
(clear b6)
)
(:goal
(and
(on b1 b5)
(on b3 b1)
(on b4 b2)
(on b5 b6)
(on b6 b7)
(on b7 b4))
)
)


