

(define (problem BW-rand-8)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 )
(:init
(arm-empty)
(on-table b1)
(on b2 b7)
(on b3 b2)
(on-table b4)
(on-table b5)
(on b6 b1)
(on-table b7)
(on b8 b4)
(clear b3)
(clear b5)
(clear b6)
(clear b8)
)
(:goal
(and
(on b1 b3)
(on b3 b7)
(on b5 b4)
(on b6 b1)
(on b8 b6))
)
)


