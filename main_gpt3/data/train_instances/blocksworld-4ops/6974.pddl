

(define (problem BW-rand-8)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 )
(:init
(arm-empty)
(on b1 b4)
(on b2 b6)
(on-table b3)
(on b4 b3)
(on b5 b8)
(on b6 b1)
(on-table b7)
(on b8 b2)
(clear b5)
(clear b7)
)
(:goal
(and
(on b2 b6)
(on b3 b2)
(on b7 b5))
)
)


